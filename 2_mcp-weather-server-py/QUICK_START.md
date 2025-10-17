# Quick Start Guide

Get your Python MCP Weather Server running in minutes!

## Prerequisites

- Python 3.10 or higher
- `uv` package manager (recommended) or `pip`

## Installation Steps

### 1. Install uv (if not already installed)

```bash
pip install uv
```

### 2. Navigate to the project directory

```bash
cd /path/to/2_mcp-weather-server-py
```

### 3. Install dependencies

```bash
uv pip install -e .
```

## Running the Server

### Option 1: Development Mode with Inspector (Recommended for Testing)

```bash
uv run mcp dev server.py
```

Open your browser to `http://localhost:6274` to access the MCP Inspector.

### Option 2: Production Mode (Stdio)

```bash
uv run server.py
```

Or use the installed script:

```bash
mcp-weather
```

## Testing Your First Tool

### Using the MCP Inspector

1. Start the server in dev mode:
   ```bash
   uv run mcp dev server.py
   ```

2. Open `http://localhost:6274` in your browser

3. Click on the "Tools" tab

4. Select the `get-weather` tool

5. Enter parameters:
   ```json
   {
     "city": "Paris"
   }
   ```

6. Click "Call Tool" and see the results!

### Using Python Client

Create a test file `test_client.py`:

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Call the get-weather tool
            result = await session.call_tool("get-weather", {"city": "Tokyo"})
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
uv run python test_client.py
```

## Next Steps

- **Integrate with Claude Desktop**: See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
- **Learn about the Inspector**: See [INSPECTOR_GUIDE.md](INSPECTOR_GUIDE.md)
- **View API documentation**: See [README.md](README.md)

## Common Issues

### Port Already in Use

If port 6274 is already in use for the Inspector:
```bash
MCP_DEV_PORT=8080 uv run mcp dev server.py
```

### Import Errors

Make sure dependencies are installed:
```bash
uv pip install -e .
```

### Python Version

Check your Python version:
```bash
python --version
```

Must be 3.10 or higher.

## Available Tools

1. **get-weather** - Get current weather for a city
   - Input: `city` (string)
   - Output: Current temperature, humidity, precipitation, weather code

2. **get-forecast** - Get 7-day forecast for a city
   - Input: `city` (string)
   - Output: Daily max/min temps, precipitation, wind, sunrise/sunset

Happy weather forecasting! 🌤️

