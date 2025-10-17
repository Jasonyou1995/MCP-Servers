# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1️⃣ Install Dependencies
```bash
cd 1_mcp-weather-server
npm install
```

### 2️⃣ Test with Inspector
```bash
npm run inspect
```
The MCP Inspector will automatically:
- Launch at `http://localhost:6274` 
- Start your weather server
- Show available tools

### 3️⃣ Try Your First Tool
1. Open browser to `http://localhost:6274`
2. Click on **`get-weather`**
3. Enter city: `"London"`
4. Click **Call Tool**
5. See live weather data! ☀️

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `npm install` | Install dependencies |
| `npm run build` | Compile TypeScript to JavaScript |
| `npm run dev` | Build and run in development mode |
| `npm start` | Run compiled production server |
| `npm run inspect` | Launch MCP Inspector for testing |

## 🛠️ Available Tools

### get-weather
**Get current weather for any city**

Example:
```json
Input:  { "city": "Tokyo" }
Output: {
  "current": {
    "temperature_2m": 18.5,
    "relative_humidity_2m": 65,
    "precipitation": 0.0
  }
}
```

### get-forecast
**Get 7-day weather forecast**

Example:
```json
Input:  { "city": "Paris" }
Output: {
  "daily": {
    "temperature_2m_max": [22.5, 23.1, 21.8, ...],
    "temperature_2m_min": [15.2, 16.3, 15.9, ...],
    "precipitation_sum": [0.0, 2.3, 0.1, ...],
    "sunrise": [...],
    "sunset": [...]
  }
}
```

## 📚 Documentation

- **[README.md](README.md)** - Complete documentation and architecture
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - IDE integration (VS Code, Claude, Cursor, etc.)
- **[INSPECTOR_GUIDE.md](INSPECTOR_GUIDE.md)** - Detailed inspector walkthrough
- **[REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)** - Code quality improvements
- **[test-tools.md](test-tools.md)** - Testing guide and examples

## 🎯 Integration with IDEs and AI Tools

After testing with the inspector, integrate with your favorite tools!

### Quick Integration
See **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** for complete instructions for:
- ✅ VS Code with GitHub Copilot
- ✅ Claude Desktop
- ✅ Cursor IDE
- ✅ Windsurf
- ✅ Cline
- ✅ Zed Editor
- ✅ Continue

### Claude Desktop Quick Setup

1. Build: `npm run build`
2. Add to config (`~/Library/Application Support/Claude/claude_desktop_config.json`):
   ```json
   {
     "mcpServers": {
       "weather": {
         "command": "node",
         "args": ["/Users/jasony/Documents/GitHub/MCP-Servers/1_mcp-weather-server/dist/main.js"]
       }
     }
   }
   ```
3. Restart Claude Desktop
4. Ask: *"What's the weather in London?"*

### VS Code with GitHub Copilot Quick Setup

1. Command Palette: `MCP: Add Server`
2. Command: `npx -y tsx main.ts`
3. Start server in MCP panel
4. Enable Agent Mode in Copilot
5. Ask: *"What's the weather in Tokyo?"*

**Full details and all platforms**: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)

## 🔧 Development Workflow

### Make Changes
```bash
# 1. Edit main.ts
code main.ts

# 2. Test with inspector
npm run inspect

# 3. Test in browser
# Open http://localhost:6274 and try tools

# 4. Build for production
npm run build
```

### Add New Tools
```typescript
// In main.ts, follow the pattern:

server.tool(
  'tool-name',
  'Description of what it does',
  {
    param: z.string().describe("Parameter description")
  },
  async({ param }) => {
    const coordinates = await fetchCityCoordinates(param);
    if (!coordinates) return createErrorResponse("Not found");
    
    const data = await fetchYourData(coordinates);
    return createSuccessResponse(data);
  }
);
```

## 🆘 Troubleshooting

### Inspector won't start?
```bash
# Try custom ports
CLIENT_PORT=8080 SERVER_PORT=9000 npm run inspect
```

### Can't find city?
```bash
# Check spelling and try variations:
# - "New York" vs "New York City"
# - "São Paulo" (with accent)
# - "London" not "Lundon"
```

### Build errors?
```bash
# Clean and reinstall
rm -rf node_modules dist
npm install
npm run build
```

## ✨ Features

- ✅ Real-time weather data from Open-Meteo API
- ✅ No API key required
- ✅ Geocoding for any city worldwide
- ✅ Current weather + 7-day forecasts
- ✅ Clean, refactored, maintainable code
- ✅ Full TypeScript support
- ✅ Interactive testing with MCP Inspector
- ✅ Production-ready

## 🎉 You're All Set!

Start testing your weather MCP server:
```bash
npm run inspect
```

Then open `http://localhost:6274` and enjoy! ☀️🌧️❄️

---

**Need help?** Check the detailed guides in the docs or open an issue.

