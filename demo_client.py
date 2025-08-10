from __future__ import annotations

import asyncio
from typing import Any

from fastmcp import Client


async def main() -> None:
    # Yerel script üzerinden stdio ile bağlan
    async with Client("server.py") as client:
        tools = await client.list_tools()
        print("Tools:", tools)

        # Örnek 1: Tümü (veya keys ile filtre)
        today = await client.call_tool(
            "finance_truncgil_get_today",
            {"keys": ["USD", "EUR"]},
        )
        print("today (USD, EUR):", today)

        # Örnek 2: Tek sembol
        usd = await client.call_tool(
            "finance_truncgil_get_symbol",
            {"symbol": "USD"},
        )
        print("USD:", usd)


if __name__ == "__main__":
    asyncio.run(main())


