"""
MCP Weather Server - Python Implementation
Provides current weather and 7-day forecast tools using the Open-Meteo API.
"""

import asyncio
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# ============================================================================
# SERVER INITIALIZATION
# ============================================================================

mcp = FastMCP("Weather Server")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def fetch_city_coordinates(city: str) -> dict[str, Any] | None:
    """
    Fetches coordinates for a given city name using the Open-Meteo Geocoding API.
    
    Args:
        city: Name of the city to geocode
        
    Returns:
        Dictionary with latitude, longitude, and name, or None if not found
    """
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        
        if not data.get("results") or len(data["results"]) == 0:
            return None
            
        result = data["results"][0]
        return {
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "name": result["name"]
        }

async def fetch_current_weather(latitude: float, longitude: float) -> dict[str, Any]:
    """
    Fetches current weather data for given coordinates.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        Weather data dictionary from Open-Meteo API
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code"
        f"&hourly=temperature_2m,precipitation"
        f"&forecast_days=1"
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def fetch_7day_forecast(latitude: float, longitude: float) -> dict[str, Any]:
    """
    Fetches 7-day weather forecast for given coordinates.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        Forecast data dictionary from Open-Meteo API
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
        f"precipitation_probability_max,weather_code,windspeed_10m_max,sunrise,sunset"
        f"&timezone=auto"
        f"&forecast_days=7"
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# ============================================================================
# TOOL DEFINITIONS
# ============================================================================

@mcp.tool(name="get-weather")
async def get_weather(city: str) -> dict[str, Any]:
    """
    Get the current weather for a city.
    
    Args:
        city: The name of the city to get the weather for
        
    Returns:
        Current weather data including temperature, humidity, precipitation, and weather code
    """
    try:
        coordinates = await fetch_city_coordinates(city)
        
        if not coordinates:
            return {
                "error": f"Sorry, I couldn't find a city named \"{city}\". Please check the spelling and try again."
            }
        
        weather_data = await fetch_current_weather(
            coordinates["latitude"],
            coordinates["longitude"]
        )
        
        return weather_data
        
    except Exception as e:
        return {
            "error": f"Error fetching weather data: {str(e)}"
        }

@mcp.tool(name="get-forecast")
async def get_forecast(city: str) -> dict[str, Any]:
    """
    Get 7-day weather forecast for a city including daily temperature, precipitation, and weather conditions.
    
    Args:
        city: The name of the city to get the forecast for
        
    Returns:
        7-day forecast data with daily max/min temperatures, precipitation, wind speed, and sunrise/sunset times
    """
    try:
        coordinates = await fetch_city_coordinates(city)
        
        if not coordinates:
            return {
                "error": f"Sorry, I couldn't find a city named \"{city}\". Please check the spelling and try again."
            }
        
        forecast_data = await fetch_7day_forecast(
            coordinates["latitude"],
            coordinates["longitude"]
        )
        
        return forecast_data
        
    except Exception as e:
        return {
            "error": f"Error fetching forecast data: {str(e)}"
        }

# ============================================================================
# SERVER EXECUTION
# ============================================================================

if __name__ == "__main__":
    mcp.run()

