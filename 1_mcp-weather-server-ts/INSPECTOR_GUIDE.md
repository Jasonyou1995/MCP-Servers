# MCP Inspector Quick Start Guide

## What You'll See

When you run `npm run inspect`, the inspector automatically:

1. ✅ Installs the Inspector tool (if needed)
2. ✅ Starts the proxy server on port 6277
3. ✅ Launches your MCP server (`main.ts`)
4. ✅ Opens the web UI at `http://localhost:6274`

## Inspector Interface Walkthrough

### 🏠 Main Screen

```
╔════════════════════════════════════════════════════════════════╗
║  MCP Inspector                                      [Settings] ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Server: Weather Server v1.0.0                    ● Connected ║
║                                                                ║
║  ┌─────────┬──────────┬─────────┬─────────┐                  ║
║  │ Tools   │ Resources│ Prompts │ Logs    │                  ║
║  └─────────┴──────────┴─────────┴─────────┘                  ║
║                                                                ║
║  Available Tools (2):                                         ║
║  ┌──────────────────────────────────────────────────────────┐ ║
║  │ 📦 get-weather                                           │ ║
║  │    Get current weather of a city                        │ ║
║  │                                                          │ ║
║  │ 📦 get-forecast                                          │ ║
║  │    Get 7-day weather forecast for a city                │ ║
║  └──────────────────────────────────────────────────────────┘ ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### 🛠️ Testing a Tool

**Step 1: Click on `get-weather` tool**

```
╔════════════════════════════════════════════════════════════════╗
║  Tool: get-weather                                   [× Close] ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Description: Tool to get the current weather of a city       ║
║                                                                ║
║  Parameters:                                                   ║
║  ┌──────────────────────────────────────────────────────────┐ ║
║  │ city (string) *required                                  │ ║
║  │ The name of the city to get the weather for             │ ║
║  │                                                          │ ║
║  │ [London_____________________________]                    │ ║
║  └──────────────────────────────────────────────────────────┘ ║
║                                                                ║
║              [Call Tool]  [Clear]  [Load Example]             ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

**Step 2: Click "Call Tool"**

```
╔════════════════════════════════════════════════════════════════╗
║  Tool Result: get-weather                                      ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ✅ Success (147ms)                                            ║
║                                                                ║
║  Response:                                                     ║
║  ┌──────────────────────────────────────────────────────────┐ ║
║  │ {                                                        │ ║
║  │   "latitude": 51.5074,                                   │ ║
║  │   "longitude": -0.1278,                                  │ ║
║  │   "current": {                                           │ ║
║  │     "temperature_2m": 15.2,                              │ ║
║  │     "relative_humidity_2m": 72,                          │ ║
║  │     "apparent_temperature": 14.1,                        │ ║
║  │     "precipitation": 0.0,                                │ ║
║  │     "weather_code": 3                                    │ ║
║  │   },                                                     │ ║
║  │   "hourly": { ... }                                      │ ║
║  │ }                                                        │ ║
║  └──────────────────────────────────────────────────────────┘ ║
║                                                                ║
║  [Copy Response]  [Call Again]  [View Raw JSON]               ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

## Common Testing Scenarios

### ✅ Test Current Weather

```bash
npm run inspect
# Browser opens automatically
# Select: get-weather
# Enter: "Tokyo"
# Click: Call Tool
# Result: Current weather for Tokyo
```

### ✅ Test 7-Day Forecast

```bash
# In the same inspector session
# Select: get-forecast
# Enter: "Paris"
# Click: Call Tool
# Result: 7-day forecast for Paris
```

### ✅ Test Error Handling

```bash
# In the same inspector session
# Select: get-weather
# Enter: "InvalidCityXYZ123"
# Click: Call Tool
# Result: Error message about city not found
```

### ✅ Test Multiple Cities

```bash
# Test rapidly without restarting:
# - London ✓
# - New York ✓
# - Singapore ✓
# - São Paulo ✓ (tests URL encoding)
```

## Inspector Features

### 📊 Real-Time Monitoring

The inspector shows:
- **Request timing** - How long each call takes
- **Connection status** - Green = connected, Red = disconnected
- **Error details** - Full stack traces when things fail
- **Request/Response logs** - Complete communication history

### 🔍 Schema Inspection

For each tool, you can view:
```json
{
  "name": "get-weather",
  "description": "Tool to get the current weather of a city",
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

### 📝 Request History

The inspector maintains a history of all calls:
- ⏱️ Timestamp
- 🛠️ Tool name
- ✅/❌ Success/Failure
- ⚡ Response time
- 📄 Full request/response data

## Tips & Tricks

### 💡 Rapid Testing
Keep the inspector open while developing. Make changes to `main.ts`, save, and refresh the inspector page to test immediately.

### 💡 Copy Configuration
Click the "Export" button to copy MCP configuration for Claude Desktop or other clients:

```json
{
  "mcpServers": {
    "weather-server": {
      "command": "node",
      "args": ["dist/main.js"]
    }
  }
}
```

### 💡 Debug Mode
Watch the terminal output where you ran `npm run inspect` to see:
- Server startup logs
- Error stack traces
- Console.log output from your server

### 💡 Network Inspector
Open browser DevTools (F12) to see:
- WebSocket/HTTP communication
- Proxy server requests
- Performance metrics

## Keyboard Shortcuts

- `Ctrl/Cmd + K` - Focus search
- `Ctrl/Cmd + Enter` - Call selected tool
- `Esc` - Close tool dialog

## Troubleshooting

### Problem: "Cannot connect to server"
**Solution:**
1. Check terminal - is the server running?
2. Look for error messages in console
3. Verify ports 6274 and 6277 are free

### Problem: "Tool call timeout"
**Solution:**
1. Check your internet connection (API calls to Open-Meteo)
2. Increase timeout in Settings
3. Check API endpoint availability

### Problem: "Invalid parameters"
**Solution:**
1. Click "View Schema" to see required fields
2. Ensure `city` is a string
3. Check for typos in parameter names

### Problem: Inspector won't start
**Solution:**
```bash
# Try with custom ports
CLIENT_PORT=8080 SERVER_PORT=9000 npm run inspect

# Or use compiled version
npm run build
npx @modelcontextprotocol/inspector node dist/main.js
```

## Comparison: Inspector vs Claude Desktop

| Feature | MCP Inspector | Claude Desktop |
|---------|---------------|----------------|
| **Purpose** | Testing & debugging | Production use |
| **Interface** | Developer UI | Chat interface |
| **Visibility** | Full request/response | Hidden details |
| **Testing** | Interactive forms | Natural language |
| **Speed** | Instant | Requires conversation |
| **Best for** | Development | End users |

## Next Steps

1. ✅ Test both tools with various cities
2. ✅ Verify error handling works
3. ✅ Check response data structure
4. ✅ Export configuration for Claude Desktop
5. ✅ Deploy to production

## Additional Resources

- [MCP Inspector GitHub](https://github.com/modelcontextprotocol/inspector)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [Model Context Protocol SDK](https://github.com/modelcontextprotocol/typescript-sdk)

---

**Happy Testing! 🎉**

The Inspector makes MCP development fast, visual, and fun!

