import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_weather_for_cities():
    """Test weather for multiple cities"""
    cities = [
        "New York",
        "Paris", 
        "Sydney",
        "Mumbai",
        "Cairo",
        "São Paulo",
        "Moscow",
        "Singapore"
    ]
    
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("🌤️  MCP Weather Server Test Results")
            print("=" * 50)
            
            for city in cities:
                try:
                    # Test current weather
                    result = await session.call_tool("get-weather", {"city": city})
                    
                    if "error" in result.content[0].text:
                        print(f"\n❌ {city}: {result.content[0].text}")
                    else:
                        weather_data = eval(result.content[0].text)
                        current = weather_data.get("current", {})
                        temp = current.get("temperature_2m", "N/A")
                        humidity = current.get("relative_humidity_2m", "N/A")
                        print(f"\n✅ {city}: {temp}°C, Humidity: {humidity}%")
                        
                    # Test 7-day forecast
                    forecast_result = await session.call_tool("get-forecast", {"city": city})
                    if "error" not in forecast_result.content[0].text:
                        forecast_data = eval(forecast_result.content[0].text)
                        daily = forecast_data.get("daily", {})
                        max_temps = daily.get("temperature_2m_max", [])
                        if max_temps:
                            print(f"   📅 7-day max temps: {max_temps[:3]}°C (first 3 days)")
                        
                except Exception as e:
                    print(f"\n❌ {city}: Error - {str(e)}")
                
                await asyncio.sleep(0.5)  # Small delay between requests

if __name__ == "__main__":
    asyncio.run(test_weather_for_cities())
