# MCP Weather Server - Tool Testing Guide

## Available Tools

### 1. get-weather
**Description:** Get current weather conditions for a city  
**Input:** `{ "city": "London" }`

**Sample Output Structure:**
```json
{
  "latitude": 51.5074,
  "longitude": -0.1278,
  "current": {
    "temperature_2m": 15.2,
    "relative_humidity_2m": 72,
    "apparent_temperature": 14.1,
    "precipitation": 0.0,
    "weather_code": 3
  },
  "hourly": {
    "temperature_2m": [...],
    "precipitation": [...]
  }
}
```

### 2. get-forecast
**Description:** Get 7-day weather forecast for a city  
**Input:** `{ "city": "Tokyo" }`

**Sample Output Structure:**
```json
{
  "latitude": 35.6895,
  "longitude": 139.6917,
  "timezone": "Asia/Tokyo",
  "daily": {
    "temperature_2m_max": [22.5, 23.1, 21.8, 20.4, 19.7, 21.2, 22.8],
    "temperature_2m_min": [15.2, 16.3, 15.9, 14.7, 13.8, 14.5, 15.9],
    "precipitation_sum": [0.0, 2.3, 0.1, 5.4, 0.0, 0.0, 1.2],
    "precipitation_probability_max": [10, 60, 20, 80, 15, 10, 30],
    "weather_code": [1, 61, 2, 63, 1, 1, 61],
    "windspeed_10m_max": [12.5, 18.3, 15.2, 22.1, 14.8, 13.2, 16.7],
    "sunrise": [...],
    "sunset": [...]
  }
}
```

## Weather Codes Reference

Common weather codes returned by Open-Meteo:
- `0`: Clear sky
- `1, 2, 3`: Mainly clear, partly cloudy, and overcast
- `45, 48`: Fog
- `51, 53, 55`: Drizzle (light, moderate, dense)
- `61, 63, 65`: Rain (slight, moderate, heavy)
- `71, 73, 75`: Snow fall (slight, moderate, heavy)
- `80, 81, 82`: Rain showers (slight, moderate, violent)
- `95, 96, 99`: Thunderstorm

## Testing Instructions

### Using MCP Inspector
1. Build the project: `npm run build`
2. Run with MCP Inspector to test both tools
3. Try different cities to verify geocoding works correctly

### Example Test Cases

**Test Case 1: Valid City**
- Tool: `get-weather`
- Input: `{ "city": "Paris" }`
- Expected: Current weather data for Paris

**Test Case 2: Invalid City**
- Tool: `get-weather`
- Input: `{ "city": "NonExistentCityXYZ" }`
- Expected: Error message about city not found

**Test Case 3: 7-Day Forecast**
- Tool: `get-forecast`
- Input: `{ "city": "New York" }`
- Expected: 7-day forecast data with daily arrays

**Test Case 4: City with Special Characters**
- Tool: `get-forecast`
- Input: `{ "city": "São Paulo" }`
- Expected: Forecast data properly geocoded with URL encoding

## Code Quality Features

✅ **Refactored Architecture:**
- Separated concerns into focused helper functions
- `fetchCityCoordinates` - Handles geocoding
- `fetchCurrentWeather` - Retrieves current weather
- `fetch7DayForecast` - Retrieves 7-day forecast
- `createErrorResponse` - Standardized error formatting
- `createSuccessResponse` - Standardized success formatting

✅ **Maintainability:**
- Clear function documentation
- Type safety with TypeScript interfaces
- DRY principle applied
- Single Responsibility Principle

✅ **Error Handling:**
- Graceful city not found handling
- Network error catching
- Type-safe error messages

✅ **Best Practices:**
- URL encoding for city names
- Const type assertions for literal types
- Proper TypeScript typing
- Clean code structure with section comments

