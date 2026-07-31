import asyncio
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schemas import AgentAction

load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


async def test_llm_structured_output():
  print("Sending prompt to Gemini...")

  prompt = "I need to calculate what 15 multiplied by 4 is."

  try:
    response = client.models.generate_content(
        model='gemini-flash-latest',  # Automatically points to the active Flash model
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=AgentAction,
            temperature=0.1,
        ),
    )

    print('\n--- Raw JSON Response Text ---')
    print(response.text)

    # Parse raw JSON string into a validated Python Pydantic object
    action_obj = AgentAction.model_validate_json(response.text)

    print('\n--- Successfully Parsed Pydantic Object! ---')
    print(f'Action Name: {action_obj.action_name}')
    print(f'Parameters:  {action_obj.parameters}')
    print(f'Reasoning:   {action_obj.reasoning}')

  except Exception as e:
    print(f'\n[API Notice]: {e}')


if __name__ == '__main__':
  asyncio.run(test_llm_structured_output())