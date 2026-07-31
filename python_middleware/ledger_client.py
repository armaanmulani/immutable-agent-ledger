import os
import httpx
from dotenv import load_dotenv

load_dotenv()


class LedgerClient:
  """Handles all HTTP communication with the Java Backend REST API."""

  def __init__(self):
    self.base_url = os.getenv(
        "JAVA_BACKEND_URL", "http://localhost:8080/api/v1/ledger"
    )

  async def get_latest_state(self) -> dict:
    """Fetches the latest verified State Block from the Java Ledger."""
    async with httpx.AsyncClient() as client:
      try:
        response = await client.get(f"{self.base_url}/latest", timeout=5.0)
        response.raise_for_status()

        # Check if response actually has content before parsing JSON
        if not response.text.strip():
          print(
              "[LedgerClient Notice] Received empty response from backend."
          )
          return {}

        return response.json()

      except httpx.HTTPError as err:
        print(f"[LedgerClient Notice] Could not connect to Java backend: {err}")
        return {}
      except ValueError as err:
        print(
            f"[LedgerClient Notice] Response was not valid JSON: {err}"
        )
        return {}

  async def commit_state_block(
      self, action_name: str, parameters: dict, observation: str
  ) -> dict:
    """Sends a proposed action + result to Java for validation & commit."""
    payload = {
        "action_name": action_name,
        "parameters": parameters,
        "observation": observation,
    }

    async with httpx.AsyncClient() as client:
      try:
        response = await client.post(
            f"{self.base_url}/commit", json=payload, timeout=5.0
        )

        if response.status_code == 400:
          print(
              "[LedgerClient] Java Validator REJECTED block:"
              f" {response.text}"
          )
          return {"status": "REJECTED", "details": response.text}

        response.raise_for_status()

        if not response.text.strip():
          return {"status": "SUCCESS", "details": {}}

        return {"status": "SUCCESS", "details": response.json()}

      except httpx.HTTPError as err:
        print(f"[LedgerClient Error] Failed to reach Java server: {err}")
        return {"status": "ERROR", "details": str(err)}
      except ValueError as err:
        print(f"[LedgerClient Error] Invalid JSON from Java server: {err}")
        return {"status": "ERROR", "details": str(err)}