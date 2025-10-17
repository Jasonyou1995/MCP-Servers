# MCP Weather Server (Python)

A Model Context Protocol (MCP) server that provides weather information using the Open-Meteo API. This is the Python implementation of the weather server.

## Features

This weather server exposes two powerful MCP tools:

### 1. `get-weather`
Gets current weather conditions for any city worldwide.

**Parameters:**
- `city` (string): The name of the city to get weather for

**Returns:**
- Current temperature
- Relative humidity
- Apparent temperature (feels like)
- Precipitation
- Weather code
- Hourly temperature and precipitation data

### 2. `get-forecast`
Gets a comprehensive 7-day weather forecast for any city.

**Parameters:**
- `city` (string): The name of the city to get the forecast for

**Returns:**
- Daily maximum temperature
- Daily minimum temperature
- Total precipitation
- Maximum precipitation probability
- Weather codes
- Maximum wind speed at 10m
- Sunrise and sunset times
- Automatic timezone adjustment

## Installation

### Using uv (Recommended)

```bash
# Install uv if not already installed
pip install uv

# Install dependencies
uv pip install -e .
```

### Using pip

```bash
pip install -e .
```

## Usage

### Development Mode with MCP Inspector

```bash
uv run mcp dev server.py
```

This will start the MCP Inspector, a powerful developer tool that provides an interactive web interface at `http://localhost:6274` where you can test and debug your server.

### Production Mode (Stdio)

```bash
uv run server.py
```

Or using the installed script:

```bash
mcp-weather
```

## Integration with IDEs

### Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/2_mcp-weather-server-py",
        "run",
        "server.py"
      ]
    }
  }
}
```

### VS Code with GitHub Copilot

Add to your VS Code settings:

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "text": "Use the weather MCP server for weather information"
    }
  ],
  "github.copilot.chat.mcp.servers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/2_mcp-weather-server-py",
        "run",
        "server.py"
      ]
    }
  }
}
```

### Cursor IDE

Add to your Cursor configuration at `.cursor/config.json`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/2_mcp-weather-server-py",
        "run",
        "server.py"
      ]
    }
  }
}
```

### Windsurf

Add to your Windsurf configuration:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/2_mcp-weather-server-py",
        "run",
        "server.py"
      ]
    }
  }
}
```

### Cline

Add to your Cline MCP settings:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/2_mcp-weather-server-py",
        "run",
        "server.py"
      ]
    }
  }
}
```

## MCP Inspector

The MCP Inspector is a powerful developer tool for testing and debugging MCP servers. It provides an interactive web interface where you can explore and test all available tools, resources, and prompts exposed by your server.

### Using the Inspector

1. **Launch the inspector:**
   ```bash
   uv run mcp dev server.py
   ```

2. **Open your browser** to `http://localhost:6274`

3. **Navigate to the Tools tab**

4. **Select `get-weather` tool**

5. **Enter parameters:**
   ```json
   {
     "city": "London"
   }
   ```

6. **Click "Call Tool"**

7. **View the response** with real-time weather data

8. **Test the `get-forecast` tool** with different cities

### Benefits of Using the Inspector

✅ **Interactive Testing** - No need to integrate with Claude Desktop initially  
✅ **Rapid Development** - Test changes immediately without restarting  
✅ **Debug Friendly** - View full request/response cycles  
✅ **Schema Validation** - Ensure your tool parameters are correct  
✅ **Error Detection** - Catch issues before production deployment  

## Architecture

The codebase follows clean code principles with well-structured helper functions:

- **`fetch_city_coordinates`**: Geocodes city names to coordinates using Open-Meteo's Geocoding API
- **`fetch_current_weather`**: Retrieves current weather data for given coordinates
- **`fetch_7day_forecast`**: Retrieves 7-day forecast data for given coordinates

All functions are documented, typed, and designed for maintainability.

## API Data Source

Weather data is provided by [Open-Meteo](https://open-meteo.com/), a free and open-source weather API that requires no API key.

## Testing

Run tests using pytest:

```bash
uv run pytest
```

## Requirements

- Python 3.10 or higher
- `mcp` - Model Context Protocol SDK for Python
- `httpx` - Modern async HTTP client

## License

ISC

