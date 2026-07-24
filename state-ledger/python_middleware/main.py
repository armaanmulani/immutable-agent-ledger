import asyncio
from ledger_client import LedgerClient


async def main():
  print("Initializing Ledger Client...")
  client = LedgerClient()

  print("Attempting to talk to Java Backend on port 8080...")
  state = await client.get_latest_state()

  print("Result received from client:", state)


if __name__ == "__main__":
  asyncio.run(main())