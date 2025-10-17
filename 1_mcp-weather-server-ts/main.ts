import {McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import {StdioServerTransport} from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from "zod";

const server = new McpServer({
  name: "Weather Server",
  version: "1.0.0",
})

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

interface GeocodingResult {
  latitude: number;
  longitude: number;
  name: string;
}

interface ToolResponse {
  [key: string]: unknown;
  content: Array<{
    type: "text";
    text: string;
  }>;
}

/**
 * Fetches coordinates for a given city name using the Open-Meteo Geocoding API
 */
async function fetchCityCoordinates(city: string): Promise<GeocodingResult | null> {
  const geoResponse = await fetch(
    `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(city)}&count=1&language=en&format=json`
  );
  const geoData = await geoResponse.json() as {
    results?: Array<{ latitude: number; longitude: number; name: string }>;
  };

  if (!geoData.results || geoData.results.length === 0) {
    return null;
  }

  const { latitude, longitude, name } = geoData.results[0];
  return { latitude, longitude, name };
}

/**
 * Creates a standardized error response for the MCP protocol
 */
function createErrorResponse(message: string): ToolResponse {
  return {
    content: [
      {
        type: "text" as const,
        text: message
      }
    ]
  };
}

/**
 * Creates a standardized success response with JSON data
 */
function createSuccessResponse(data: any): ToolResponse {
  return {
    content: [
      {
        type: "text" as const,
        text: JSON.stringify(data, null, 2)
      }
    ]
  };
}

/**
 * Fetches current weather data for given coordinates
 */
async function fetchCurrentWeather(latitude: number, longitude: number): Promise<any> {
  const weatherResponse = await fetch(
    `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code&hourly=temperature_2m,precipitation&forecast_days=1`
  );
  return await weatherResponse.json();
}

/**
 * Fetches 7-day weather forecast for given coordinates
 */
async function fetch7DayForecast(latitude: number, longitude: number): Promise<any> {
  const forecastResponse = await fetch(
    `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,weather_code,windspeed_10m_max,sunrise,sunset&timezone=auto&forecast_days=7`
  );
  return await forecastResponse.json();
}

// ============================================================================
// TOOL DEFINITIONS
// ============================================================================

/**
 * Tool: get-weather
 * Gets current weather for a specified city
 */
server.tool(
  'get-weather',
  'Tool to get the current weather of a city',
  {
    city: z.string().describe("The name of the city to get the weather for")
  },
  async({ city }) => {
    try {
      const coordinates = await fetchCityCoordinates(city);
      
      if (!coordinates) {
        return createErrorResponse(
          `Sorry, I couldn't find a city named "${city}". Please check the spelling and try again.`
        );
      }

      const weatherData = await fetchCurrentWeather(coordinates.latitude, coordinates.longitude);
      return createSuccessResponse(weatherData);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      return createErrorResponse(`Error fetching weather data: ${errorMessage}`);
    }
  }
);

/**
 * Tool: get-forecast
 * Gets 7-day weather forecast for a specified city
 */
server.tool(
  'get-forecast',
  'Get 7-day weather forecast for a city including daily temperature, precipitation, and weather conditions',
  {
    city: z.string().describe("The name of the city to get the forecast for")
  },
  async({ city }) => {
    try {
      const coordinates = await fetchCityCoordinates(city);
      
      if (!coordinates) {
        return createErrorResponse(
          `Sorry, I couldn't find a city named "${city}". Please check the spelling and try again.`
        );
      }

      const forecastData = await fetch7DayForecast(coordinates.latitude, coordinates.longitude);
      return createSuccessResponse(forecastData);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      return createErrorResponse(`Error fetching forecast data: ${errorMessage}`);
    }
  }
);

// ============================================================================
// SERVER INITIALIZATION
// ============================================================================

const transport = new StdioServerTransport();
server.connect(transport);

