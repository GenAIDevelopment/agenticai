import asyncio
from fastmcp import Client
from fastmcp.transports.http import StreamableHttpTransport

SERVER_URL = "http://localhost:18000/mcp"

async def main():
    # 1️⃣ Perform login first
    transport = StreamableHttpTransport(SERVER_URL)
    async with Client(transport) as client:
        login_result = await client.call_tool(
            "login", {"username": "khaja", "password": "password123"}
        )

        if login_result.is_error:
            print("Login failed:", login_result.error)
            return

        token = login_result.data["session_token"]
        print("Login successful, token:", token)

    # 2️⃣ Connect again with Authorization header for subsequent tools
    headers = {"Authorization": f"Bearer {token}"}
    transport_auth = StreamableHttpTransport(SERVER_URL, headers=headers)
    async with Client(transport_auth) as auth_client:
        whoami_result = await auth_client.call_tool("whoami", {})
        if whoami_result.is_error:
            print("Whoami failed:", whoami_result.error)
        else:
            print("Whoami result:", whoami_result.data)

if __name__ == "__main__":
    asyncio.run(main())
