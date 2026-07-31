import asyncio
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from schemas import AgentAction
from tools import dispatch_action

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


async def run_agent_step(user_prompt: str):
  print(f"\n==========================================")
  print(f"User Prompt: '{user_prompt}'")
  print("1. Sending prompt to Gemini for decision...")

  try:
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are an AI Agent middleware controller. Output valid JSON"
                " strictly adhering to the schema. When providing Python code,"
                " escape all newlines as '\\n' so the JSON remains strictly"
                " valid."
            ),
            response_mime_type="application/json",
            response_schema=AgentAction,
            temperature=0.1,
            max_output_tokens=2048,
        ),
    )

    action = AgentAction.model_validate_json(response.text)

    print("\n--- AI Decision ---")
    print(f"Chosen Action: {action.action_name}")
    print(f"Reasoning:     {action.reasoning}")
    print(f"Parameters:    {action.parameters}")

    print("\n2. Executing tool in Python environment...")
    observation = dispatch_action(action.action_name, action.parameters)

    print("\n--- Real World Observation ---")
    print(observation)

  except Exception as e:
    print(f"\n[Execution Error]: {e}")


async def main():
  # Test 1: Python Interpreter
  await run_agent_step(
      "Write a script to reverse the string 'ImmutableStateLedger' and print"
      " its vowels."
  )


if __name__ == "__main__":
  asyncio.run(main())