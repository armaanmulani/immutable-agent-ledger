import httpx
from typing import Any, Dict, Optional

BASE_URL = "https://state-ledger-service-336798788711.us-central1.run.app"

class LedgerClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    async def get_latest_state(self) -> Optional[Dict[str, Any]]:
        """Fetches the latest state block from the immutable ledger."""
        url = f"{self.base_url}/api/ledger/latest"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=10.0)
                if response.status_code == 200:
                    return response.json()
                print(f"[Ledger Status {response.status_code}] Latest state response: {response.text}")
                return None
            except Exception as e:
                print(f"[Ledger Client Error] Failed to fetch latest state: {e}")
                return None

    async def commit_block(
        self,
        action_type: str,
        parameters: Dict[str, Any],
        status: str = "SUCCESS",
        environment: str = "development",
        session_id: str = "test_session_01"
    ) -> Optional[Dict[str, Any]]:
        """Commits a new action and execution state to the ledger via POST."""
        url = f"{self.base_url}/api/ledger/commit"
        
        payload = {
            "action_intent": {
                "action_type": action_type.upper(),
                "parameters": parameters
            },
            "system_context": {
                "environment": environment,
                "session_id": session_id
            },
            "execution_result": {
                "status": status
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, timeout=10.0)
                if response.status_code in (200, 201):
                    return response.json()
                
                print(f"\n[Backend Error {response.status_code}]: Detailed Response: {response.text}")
                return None
            except Exception as e:
                print(f"[Ledger Client Error] Request failed: {e}")
                return None