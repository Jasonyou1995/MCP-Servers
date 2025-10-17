# MCP Inspector Guide

The MCP Inspector is a powerful developer tool for testing and debugging MCP servers. This guide explains how to use it with the Python Weather Server.

## What is the MCP Inspector?

The MCP Inspector is a web-based development tool that provides an interactive interface for testing MCP servers without needing to integrate them with AI applications first.

### Components

The Inspector consists of two parts:

1. **Web UI (Client)** - A React-based interface running at `http://localhost:6274`
2. **Proxy Server** - A Node.js proxy that bridges browser and server communication

### Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Browser   │◄────►│  MCP Proxy   │◄────►│ MCP Server  │
│  (Port 6274)│ HTTP │  (Port 6277) │ STDIO│ (server.py) │
└─────────────┘      └──────────────┘      └─────────────┘
```

## Starting the Inspector

### Basic Usage

```bash
uv run mcp dev server.py
```

This will:
1. Start your Python MCP weather server
2. Launch the Inspector proxy
3. Open the web interface at `http://localhost:6274`

### Custom Port

```bash
MCP_DEV_PORT=8080 uv run mcp dev server.py
```

### With Debug Logging

```bash
DEBUG=1 uv run mcp dev server.py
```

## Using the Inspector Interface

### 1. Server Info Tab

When you first open the Inspector, you'll see the Server Info tab:

- **Server Name**: "Weather Server"
- **Server Version**: "1.0.0"
- **Connection Status**: Connected/Disconnected
- **Capabilities**: Lists what the server can do
- **Protocol Version**: MCP protocol version

### 2. Tools Tab

This is where you'll spend most of your time testing.

#### Viewing Tools

You'll see two tools listed:
- **get-weather** - Get current weather for a city
- **get-forecast** - Get 7-day forecast for a city

#### Testing get-weather

1. Click on "get-weather" in the tools list
2. You'll see the tool's description and parameters
3. In the parameters section, enter:
   ```json
   {
     "city": "London"
   }
   ```
4. Click "Call Tool"
5. View the response in JSON format

**Example Response:**
```json
{
  "latitude": 51.5074,
  "longitude": -0.1278,
  "current": {
    "time": "2025-10-17T12:00",
    "temperature_2m": 15.2,
    "relative_humidity_2m": 72,
    "apparent_temperature": 14.1,
    "precipitation": 0.0,
    "weather_code": 2
  },
  "hourly": {
    "time": [...],
    "temperature_2m": [...],
    "precipitation": [...]
  }
}
```

#### Testing get-forecast

1. Click on "get-forecast" in the tools list
2. Enter parameters:
   ```json
   {
     "city": "Paris"
   }
   ```
3. Click "Call Tool"
4. View the 7-day forecast response

**Example Response:**
```json
{
  "latitude": 48.8566,
  "longitude": 2.3522,
  "timezone": "Europe/Paris",
  "daily": {
    "time": ["2025-10-17", "2025-10-18", ...],
    "temperature_2m_max": [18.5, 19.2, ...],
    "temperature_2m_min": [12.3, 13.1, ...],
    "precipitation_sum": [0.0, 2.5, ...],
    "precipitation_probability_max": [10, 60, ...],
    "weather_code": [1, 61, ...],
    "windspeed_10m_max": [15.2, 18.5, ...],
    "sunrise": ["2025-10-17T07:45", ...],
    "sunset": ["2025-10-17T18:30", ...]
  }
}
```

### 3. Resources Tab

The weather server doesn't expose resources, so this tab will be empty.

### 4. Prompts Tab

The weather server doesn't define prompts, so this tab will be empty.

## Testing Scenarios

### Test Case 1: Valid City

**Tool**: get-weather  
**Input**: `{"city": "Tokyo"}`  
**Expected**: Successful response with current weather data

### Test Case 2: Invalid City

**Tool**: get-weather  
**Input**: `{"city": "InvalidCityName123"}`  
**Expected**: Error response with message about city not found

### Test Case 3: Special Characters

**Tool**: get-weather  
**Input**: `{"city": "São Paulo"}`  
**Expected**: Successful response (geocoding should handle special characters)

### Test Case 4: Multiple Word City

**Tool**: get-forecast  
**Input**: `{"city": "New York"}`  
**Expected**: Successful 7-day forecast response

### Test Case 5: Different Languages

**Tool**: get-weather  
**Input**: `{"city": "München"}` (German name for Munich)  
**Expected**: Successful response (geocoding API supports multiple languages)

## Debugging with the Inspector

### Viewing Request/Response

The Inspector shows:
- **Request parameters**: What you sent to the tool
- **Response data**: The complete JSON response
- **Execution time**: How long the tool took to execute
- **Error messages**: If something went wrong

### Common Issues

#### 1. Server Not Starting

**Symptom**: Inspector shows "Connection Failed"

**Solutions**:
- Check that `server.py` has no syntax errors
- Verify dependencies are installed: `uv pip install -e .`
- Look at terminal output for error messages

#### 2. Tool Execution Errors

**Symptom**: Red error message in response

**Solutions**:
- Check the error message details
- Verify your internet connection (needed for Open-Meteo API)
- Try a different city name

#### 3. Slow Responses

**Symptom**: Tool takes a long time to respond

**Possible Causes**:
- Slow internet connection
- Open-Meteo API experiencing high load
- Network issues

### Inspecting Tool Schemas

Click on any tool to see its full schema:

```json
{
  "name": "get-weather",
  "description": "Get the current weather for a city.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "The name of the city to get the weather for"
      }
    },
    "required": ["city"]
  }
}
```

This helps you understand:
- What parameters are required
- What data types are expected
- Parameter descriptions

## Advanced Inspector Features

### Network Tab (Browser DevTools)

Open your browser's DevTools (F12) to see:
- HTTP requests between browser and proxy
- WebSocket connections
- Network timing

### Console Logging

Add print statements to your server code:

```python
@mcp.tool()
async def get_weather(city: str) -> dict[str, Any]:
    print(f"DEBUG: Fetching weather for {city}")
    # ... rest of the code
```

These will appear in the terminal where you ran `uv run mcp dev server.py`.

### Testing Error Handling

Intentionally trigger errors to test error handling:

1. **Invalid JSON**: Enter malformed JSON in parameters
2. **Missing Required Field**: Omit the `city` parameter
3. **Wrong Data Type**: Use a number instead of a string for city

## Rapid Development Workflow

1. **Make changes** to `server.py`
2. **Stop the Inspector** (Ctrl+C in terminal)
3. **Restart**: `uv run mcp dev server.py`
4. **Refresh browser** (if needed)
5. **Test your changes** immediately

### Hot Reload (Future)

Currently, you need to restart the server for changes to take effect. Watch for future updates to the MCP SDK that may include hot reload functionality.

## Comparison with Production

### Inspector (Development)

- Interactive web interface
- Manual tool invocation
- Visual response inspection
- Immediate feedback
- Good for testing and debugging

### Production (Claude Desktop, etc.)

- AI automatically calls tools
- Tools invoked based on user questions
- Responses fed back to AI
- Integrated user experience
- Good for end users

## Next Steps

After testing with the Inspector:

1. ✅ Verify both tools work correctly
2. ✅ Test edge cases (invalid cities, special characters)
3. ✅ Check error handling
4. 📝 Document any issues found
5. 🚀 Integrate with Claude Desktop or other AI tools

See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for integration instructions.

## Additional Resources

- [MCP Inspector Documentation](https://github.com/modelcontextprotocol/inspector)
- [MCP Python SDK Documentation](https://github.com/modelcontextprotocol/python-sdk)
- [Open-Meteo API Documentation](https://open-meteo.com/en/docs)

