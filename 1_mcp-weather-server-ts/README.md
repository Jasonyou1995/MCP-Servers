# MCP Weather Server

A Model Context Protocol (MCP) server that provides weather information using the Open-Meteo API.

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

```bash
npm install
```

## Build

```bash
npm run build
```

## Usage

### Development Mode
```bash
npm run dev
```

### Production Mode
```bash
npm start
```

### Testing with MCP Inspector
```bash
npm run inspect
```

### Integration with IDEs
See **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** for complete instructions on integrating with:
- VS Code with GitHub Copilot
- Claude Desktop
- Cursor IDE
- Windsurf
- Cline
- Zed Editor
- Continue

## MCP Inspector

The MCP Inspector is a powerful developer tool for testing and debugging MCP servers. It provides an interactive web interface where you can explore and test all available tools, resources, and prompts exposed by your server.

### What is the MCP Inspector?

The MCP Inspector consists of two main components:

1. **Web UI (Client)** - A React-based interface running at `http://localhost:6274`
2. **Proxy Server** - A Node.js proxy server running at port `6277` that bridges browser and MCP server communication

### How It Works

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Browser   │◄────►│  MCP Proxy   │◄────►│ MCP Server  │
│  (Port 6274)│ HTTP │  (Port 6277) │ STDIO│ (main.ts)   │
└─────────────┘      └──────────────┘      └─────────────┘
```

1. **You launch the inspector** with `npm run inspect`
2. **The proxy server starts** and spawns your MCP server (`tsx main.ts`)
3. **Communication flow**:
   - Your browser connects to the web UI at `http://localhost:6274`
   - The UI sends tool requests to the proxy server
   - The proxy translates HTTP requests to STDIO communication
   - Your MCP server receives and processes the requests
   - Responses flow back through the proxy to the UI

### Using the Inspector

Once launched, the Inspector UI provides:

#### 🛠️ Tools Tab
- **View all available tools** (`get-weather`, `get-forecast`)
- **Inspect tool schemas** - See parameter definitions and descriptions
- **Test tools interactively** - Fill in parameters and execute calls
- **View responses** - See formatted JSON responses in real-time

#### 📚 Resources Tab (if applicable)
- List and read any resources exposed by your server

#### 💬 Prompts Tab (if applicable)
- View and test prompt templates

#### ⚙️ Server Info
- View server metadata (name, version)
- Monitor connection status
- Check server capabilities

### Example Testing Workflow

1. **Launch the inspector:**
   ```bash
   npm run inspect
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

7. **View the response:**
   ```json
   {
     "latitude": 51.5074,
     "longitude": -0.1278,
     "current": {
       "temperature_2m": 15.2,
       "relative_humidity_2m": 72,
       ...
     }
   }
   ```

8. **Test the `get-forecast` tool** with different cities

### Inspector Command Breakdown

```bash
npx -y @modelcontextprotocol/inspector npx -y tsx main.ts
```

- `npx -y @modelcontextprotocol/inspector` - Runs the Inspector package (auto-installs if needed)
- `npx -y tsx main.ts` - The command the Inspector uses to start your server
  - `tsx` - TypeScript executor (runs `.ts` files directly)
  - `main.ts` - Your MCP server source file

### Advanced Inspector Features

#### Custom Ports
```bash
CLIENT_PORT=8080 SERVER_PORT=9000 npm run inspect
```

#### Environment Variables
```bash
npx @modelcontextprotocol/inspector -e API_KEY=secret npx tsx main.ts
```

#### Network Access
```bash
HOST=0.0.0.0 npm run inspect
```
*⚠️ Only use in trusted networks*

### Benefits of Using the Inspector

✅ **Interactive Testing** - No need to integrate with Claude Desktop initially  
✅ **Rapid Development** - Test changes immediately without restarting  
✅ **Debug Friendly** - View full request/response cycles  
✅ **Schema Validation** - Ensure your tool parameters are correct  
✅ **Error Detection** - Catch issues before production deployment  

### Troubleshooting

**Port already in use:**
```bash
CLIENT_PORT=8080 SERVER_PORT=9000 npm run inspect
```

**TypeScript errors:**
- Ensure `tsx` is available: `npm install -g tsx`
- Or use the compiled version: `npx @modelcontextprotocol/inspector node dist/main.js`

**Can't connect:**
- Check that ports 6274 and 6277 are not blocked by firewall
- Verify the server is running (check terminal output)
- Try refreshing the browser

For more information, visit the [MCP Inspector documentation](https://github.com/modelcontextprotocol/inspector).

## Architecture

The codebase follows clean code principles with well-structured helper functions:

- **`fetchCityCoordinates`**: Geocodes city names to coordinates using Open-Meteo's Geocoding API
- **`fetchCurrentWeather`**: Retrieves current weather data for given coordinates
- **`fetch7DayForecast`**: Retrieves 7-day forecast data for given coordinates
- **`createErrorResponse`**: Standardized error response formatter
- **`createSuccessResponse`**: Standardized success response formatter

All functions are documented, typed, and designed for maintainability.

## API Data Source

Weather data is provided by [Open-Meteo](https://open-meteo.com/), a free and open-source weather API that requires no API key.

## License

ISC

