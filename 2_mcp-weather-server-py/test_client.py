import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Call the get-weather tool
            result = await session.call_tool("get-weather", {"city": "Tokyo"})
            print("Tokyo Weather:")
            print(result)
            
            # Test another city
            result = await session.call_tool("get-weather", {"city": "London"})
            print("\nLondon Weather:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
