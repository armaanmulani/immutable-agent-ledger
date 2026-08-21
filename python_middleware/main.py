import os
import asyncio
from dotenv import load_dotenv
from google import genai
from google.genai import types

from schemas import AgentAction
from tools import dispatch_action
from ledger_client import LedgerClient

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
ledger_client = LedgerClient()

MODEL_NAME = "gemini-3.6-flash"


async def run_agent_turn(user_prompt: str, session_id: str = "session_azaan_01"):
    print("\n" + "=" * 60)
    print(f"User Prompt: '{user_prompt}'")
    
    # 1. Fetch Verified State from Cloud Run
    print("\n1. Injecting cryptographically verified state from Ledger...")
    latest_state = await ledger_client.get_latest_state()
    
    if latest_state:
        block_id = latest_state.get("blockId", "N/A")
        curr_hash = latest_state.get("currentHash", "")
        last_intent = latest_state.get("actionIntent", {})
        last_status = latest_state.get("status", "UNKNOWN")
        print(f"   [State Injected] Block #{block_id} | Hash: {curr_hash[:12]}... | Last Status: {last_status}")
        
        context_str = (
            f"Current Verified Ledger State:\n"
            f"- Last Block ID: {block_id}\n"
            f"- Last Block Hash: {curr_hash}\n"
            f"- Last Action: {last_intent.get('action_type', 'NONE')} with params {last_intent.get('parameters', {})}\n"
            f"- Ledger Status: {last_status}\n"
        )
    else:
        context_str = "No prior ledger state found. Starting fresh session.\n"

    # 2. Decision Step with Grounded Context
    print("2. Sending prompt to Gemini with injected state context...")
    system_instruction = f"""
You are an AI Agent middleware controller backed by an immutable cryptographic state ledger.
You must strictly output valid JSON adhering to the provided schema.

{context_str}

Available Actions:
- 'SEARCH': Use for web queries, information retrieval, and general tasks. Pass the query string in parameters.query.
"""
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=AgentAction,
                temperature=0.1,
                max_output_tokens=2048
            )
        )

        action = AgentAction.model_validate_json(response.text)
        print(f"   [Decision] Action: {action.action_name}")
        print(f"   [Parameters]: {action.parameters.query}")
        print(f"   [Reasoning]:  {action.reasoning}")

        # 3. Tool Execution
        print("\n3. Executing tool in Python environment...")
        observation = dispatch_action(action.action_name, action.parameters)
        print(f"   [Observation Preview]:\n{observation[:250]}...\n")

        # 4. Commit to Live Cloud Run Ledger
        print("4. Committing state block to Cloud Run Ledger...")
        params_dict = action.parameters.model_dump(exclude_none=True)
        commit_status = "FAILURE" if observation.startswith("Error") else "SUCCESS"
        
        commit_res = await ledger_client.commit_block(
            action_type=action.action_name,
            parameters=params_dict,
            status=commit_status,
            environment="production",
            session_id=session_id
        )

        # 5. Rollback / Intercept Check
        if not commit_res or commit_res.get("status") == "REJECTED":
            print("\n[SECURITY INTERCEPT] Ledger rejected state change! State rolled back.")
            reason = commit_res.get("reason", "Unknown rejection") if commit_res else "Network error"
            print(f"Reason: {reason}")
            return

        print(f"   [Committed] Block #{commit_res.get('blockId')} | New Hash: {commit_res.get('currentHash')[:12]}...")

        # 6. Final Answer Synthesis
        print("\n5. Synthesizing final response for user...")
        synthesis_prompt = f"""
User Query: {user_prompt}
Tool Executed: {action.action_name}
Observation Data:
{observation}

Provide a direct, concise summary to answer the user query based on the observation data.
"""
        final_answer = client.models.generate_content(
            model=MODEL_NAME,
            contents=synthesis_prompt
        )

        print("\n" + "=" * 60)
        print("AGENT FINAL ANSWER:")
        print(final_answer.text)
        print("=" * 60)

    except Exception as e:
        print(f"\n[Execution Error]: {e}")


async def main():
    print("Autonomous State-Ledger Agent REPL")
    print("Type your prompt or type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                print("Session ended.")
                break
            
            await run_agent_turn(user_input)
        except KeyboardInterrupt:
            print("\nSession interrupted. Exiting...")
            break

if __name__ == "__main__":
    asyncio.run(main())