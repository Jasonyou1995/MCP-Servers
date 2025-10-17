"""
Example test script for the MCP Weather Server.
This demonstrates how to test the server programmatically.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_list_tools():
    """Test listing available tools"""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"]
    )
    
    print("=" * 60)
    print("Testing: List Available Tools")
    print("=" * 60)
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            tools = await session.list_tools()
            print(f"\nFound {len(tools.tools)} tools:\n")
            for tool in tools.tools:
                print(f"  📋 {tool.name}")
                print(f"     Description: {tool.description}\n")


async def test_get_weather():
    """Test the get-weather tool"""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"]
    )
    
    print("=" * 60)
    print("Testing: get-weather Tool")
    print("=" * 60)
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            test_city = "London"
            print(f"\nFetching weather for: {test_city}")
            print("-" * 60)
            
            result = await session.call_tool("get-weather", {"city": test_city})
            
            # Check if we have structured content (MCP 2025-06-18 spec)
            if result.structuredContent:
                data = result.structuredContent
                if "error" in data:
                    print(f"❌ Error: {data['error']}")
                else:
                    print(f"✅ Success!")
                    print(f"   Latitude: {data.get('latitude', 'N/A')}")
                    print(f"   Longitude: {data.get('longitude', 'N/A')}")
                    if 'current' in data:
                        current = data['current']
                        print(f"   Temperature: {current.get('temperature_2m', 'N/A')}°C")
                        print(f"   Humidity: {current.get('relative_humidity_2m', 'N/A')}%")
                        print(f"   Precipitation: {current.get('precipitation', 'N/A')} mm")
            else:
                print("Response (text content):", result.content)


async def test_get_forecast():
    """Test the get-forecast tool"""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"]
    )
    
    print("\n" + "=" * 60)
    print("Testing: get-forecast Tool")
    print("=" * 60)
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            test_city = "Paris"
            print(f"\nFetching 7-day forecast for: {test_city}")
            print("-" * 60)
            
            result = await session.call_tool("get-forecast", {"city": test_city})
            
            # Check if we have structured content
            if result.structuredContent:
                data = result.structuredContent
                if "error" in data:
                    print(f"❌ Error: {data['error']}")
                else:
                    print(f"✅ Success!")
                    print(f"   Latitude: {data.get('latitude', 'N/A')}")
                    print(f"   Longitude: {data.get('longitude', 'N/A')}")
                    print(f"   Timezone: {data.get('timezone', 'N/A')}")
                    if 'daily' in data:
                        daily = data['daily']
                        days = len(daily.get('time', []))
                        print(f"   Forecast days: {days}")
                        if days > 0:
                            print(f"\n   First day forecast:")
                            print(f"   - Date: {daily['time'][0] if 'time' in daily else 'N/A'}")
                            print(f"   - Max temp: {daily['temperature_2m_max'][0] if 'temperature_2m_max' in daily else 'N/A'}°C")
                            print(f"   - Min temp: {daily['temperature_2m_min'][0] if 'temperature_2m_min' in daily else 'N/A'}°C")
                            print(f"   - Precipitation: {daily['precipitation_sum'][0] if 'precipitation_sum' in daily else 'N/A'} mm")
            else:
                print("Response (text content):", result.content)


async def main():
    """Run all tests"""
    print("\n🌤️  MCP Weather Server - Example Tests\n")
    
    try:
        await test_list_tools()
        await test_get_weather()
        await test_get_forecast()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}\n")
        raise


if __name__ == "__main__":
    asyncio.run(main())

