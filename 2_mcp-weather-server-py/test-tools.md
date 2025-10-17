# Testing MCP Tools

Comprehensive guide for testing the Python MCP Weather Server tools.

## Testing Methods

### 1. MCP Inspector (Recommended)

The easiest way to test your tools interactively.

```bash
uv run mcp dev server.py
```

Open `http://localhost:6274` and use the web interface.

### 2. Python Client Script

Create a test script to programmatically test tools.

#### Example: test_weather.py

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_get_weather():
    """Test the get-weather tool"""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test with a valid city
            print("Testing get-weather with 'London'...")
            result = await session.call_tool("get-weather", {"city": "London"})
            print("Response:", result)
            print()
            
            # Test with an invalid city
            print("Testing get-weather with invalid city...")
            result = await session.call_tool("get-weather", {"city": "InvalidCity123"})
            print("Response:", result)


async def test_get_forecast():
    """Test the get-forecast tool"""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test forecast
            print("Testing get-forecast with 'Paris'...")
            result = await session.call_tool("get-forecast", {"city": "Paris"})
            print("Response:", result)


async def test_list_tools():
    """List all available tools"""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")


async def main():
    """Run all tests"""
    print("=" * 60)
    print("MCP Weather Server - Tool Tests")
    print("=" * 60)
    print()
    
    await test_list_tools()
    print()
    
    await test_get_weather()
    print()
    
    await test_get_forecast()
    print()
    
    print("=" * 60)
    print("Tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
uv run python test_weather.py
```

### 3. Unit Tests with Pytest

Create proper unit tests for production use.

#### Example: test_server.py

```python
import pytest
from collections.abc import AsyncGenerator
from mcp.client.session import ClientSession
from mcp.shared.memory import create_connected_server_and_client_session
from mcp.types import CallToolResult, TextContent

from server import mcp as app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client_session() -> AsyncGenerator[ClientSession]:
    async with create_connected_server_and_client_session(
        app, raise_exceptions=True
    ) as _session:
        yield _session


@pytest.mark.anyio
async def test_list_tools(client_session: ClientSession):
    """Test that tools are correctly registered"""
    tools = await client_session.list_tools()
    tool_names = [tool.name for tool in tools.tools]
    
    assert "get-weather" in tool_names
    assert "get-forecast" in tool_names


@pytest.mark.anyio
async def test_get_weather_valid_city(client_session: ClientSession):
    """Test get-weather with a valid city"""
    result = await client_session.call_tool("get-weather", {"city": "London"})
    
    # Check that we got a result
    assert result.content
    
    # If there's structured content, check it
    if result.structuredContent:
        assert "latitude" in result.structuredContent
        assert "longitude" in result.structuredContent


@pytest.mark.anyio
async def test_get_weather_invalid_city(client_session: ClientSession):
    """Test get-weather with an invalid city"""
    result = await client_session.call_tool("get-weather", {"city": "InvalidCity123"})
    
    # Should return an error message
    assert result.content
    if result.structuredContent:
        assert "error" in result.structuredContent


@pytest.mark.anyio
async def test_get_forecast_valid_city(client_session: ClientSession):
    """Test get-forecast with a valid city"""
    result = await client_session.call_tool("get-forecast", {"city": "Paris"})
    
    # Check that we got a result
    assert result.content
    
    # If there's structured content, check for forecast data
    if result.structuredContent:
        assert "latitude" in result.structuredContent
        assert "longitude" in result.structuredContent
        # Forecast should have daily data
        if "daily" in result.structuredContent:
            daily = result.structuredContent["daily"]
            assert "temperature_2m_max" in daily
            assert "temperature_2m_min" in daily
```

Run tests:
```bash
uv run pytest test_server.py -v
```

## Test Cases

### get-weather Tool

#### Test Case 1: Valid Major City
```json
{
  "city": "London"
}
```
**Expected**: Weather data with temperature, humidity, precipitation

#### Test Case 2: City with Spaces
```json
{
  "city": "New York"
}
```
**Expected**: Weather data for New York

#### Test Case 3: City with Special Characters
```json
{
  "city": "São Paulo"
}
```
**Expected**: Weather data handling UTF-8 characters

#### Test Case 4: City in Different Language
```json
{
  "city": "München"
}
```
**Expected**: Weather data (geocoding should handle German name)

#### Test Case 5: Invalid City
```json
{
  "city": "InvalidCityName123"
}
```
**Expected**: Error message about city not found

#### Test Case 6: Empty String
```json
{
  "city": ""
}
```
**Expected**: Error or no results

### get-forecast Tool

#### Test Case 1: Valid City
```json
{
  "city": "Tokyo"
}
```
**Expected**: 7-day forecast with daily data

#### Test Case 2: Southern Hemisphere City
```json
{
  "city": "Sydney"
}
```
**Expected**: Forecast with appropriate timezone

#### Test Case 3: Small City
```json
{
  "city": "Reykjavik"
}
```
**Expected**: Valid forecast data

#### Test Case 4: Invalid City
```json
{
  "city": "NotARealCity999"
}
```
**Expected**: Error message

## Manual Testing Checklist

Before deploying or integrating:

- [ ] Test get-weather with at least 5 different cities
- [ ] Test get-weather with invalid city name
- [ ] Test get-forecast with at least 3 different cities
- [ ] Test get-forecast with invalid city name
- [ ] Verify error handling for network issues (disconnect internet temporarily)
- [ ] Check response times (should be < 2 seconds typically)
- [ ] Test with cities in different timezones
- [ ] Test with cities in different hemispheres
- [ ] Verify UTF-8 character handling
- [ ] Check that all required fields are present in responses

## Performance Testing

### Response Time Test

```python
import asyncio
import time
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def measure_response_time():
    """Measure tool response times"""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test get-weather
            start = time.time()
            await session.call_tool("get-weather", {"city": "London"})
            weather_time = time.time() - start
            print(f"get-weather response time: {weather_time:.2f}s")
            
            # Test get-forecast
            start = time.time()
            await session.call_tool("get-forecast", {"city": "Paris"})
            forecast_time = time.time() - start
            print(f"get-forecast response time: {forecast_time:.2f}s")


asyncio.run(measure_response_time())
```

Expected times:
- **get-weather**: 0.5-2 seconds
- **get-forecast**: 0.5-2 seconds

If consistently slower, check:
- Internet connection speed
- Open-Meteo API status
- Network latency

## Error Testing

### Test Network Failures

Temporarily disconnect internet and test:

```python
async def test_network_failure():
    """Test behavior when network is unavailable"""
    # Disconnect internet before running this
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result = await session.call_tool("get-weather", {"city": "London"})
            print("Result:", result)
            # Should get an error about connection


asyncio.run(test_network_failure())
```

Expected: Error message about connection failure

### Test Invalid Input Types

The MCP SDK should validate input types, but you can test edge cases:

```python
# These should be rejected by the SDK before reaching your tool
await session.call_tool("get-weather", {"city": 123})  # Number instead of string
await session.call_tool("get-weather", {"city": None})  # None value
await session.call_tool("get-weather", {})  # Missing required parameter
```

## Debugging Failed Tests

### 1. Check Server Logs

Run the server manually to see error messages:
```bash
uv run server.py
```

### 2. Add Debug Logging

Modify `server.py` to add logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@mcp.tool()
async def get_weather(city: str) -> dict[str, Any]:
    logger.debug(f"get_weather called with city: {city}")
    # ... rest of the code
```

### 3. Test Individual Functions

Test helper functions directly:

```python
import asyncio
from server import fetch_city_coordinates, fetch_current_weather

async def test_helpers():
    coords = await fetch_city_coordinates("London")
    print("Coordinates:", coords)
    
    if coords:
        weather = await fetch_current_weather(
            coords["latitude"],
            coords["longitude"]
        )
        print("Weather:", weather)

asyncio.run(test_helpers())
```

### 4. Verify Dependencies

```bash
uv pip list | grep -E "(mcp|httpx)"
```

Should show:
- mcp >= 1.1.4
- httpx >= 0.28.1

## Continuous Testing

### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "Running tests before commit..."
uv run pytest test_server.py
if [ $? -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

### CI/CD Pipeline

Example GitHub Actions workflow (`.github/workflows/test.yml`):

```yaml
name: Test MCP Server

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install uv
        run: pip install uv
      - name: Install dependencies
        run: uv pip install -e .[dev]
      - name: Run tests
        run: uv run pytest test_server.py -v
```

## Test Coverage

To measure test coverage:

```bash
uv pip install pytest-cov
uv run pytest test_server.py --cov=server --cov-report=html
```

Open `htmlcov/index.html` to see coverage report.

Aim for:
- **90%+ coverage** of tool functions
- **80%+ coverage** of helper functions
- **100% coverage** of error handling paths

## Troubleshooting Tests

### Tests Hang

- Check that the server starts properly
- Verify no port conflicts
- Ensure internet connectivity for API tests

### Inconsistent Results

- Open-Meteo API returns real-time data
- Use mocking for deterministic tests
- Cache responses for repeated tests

### Import Errors

```bash
uv pip install -e .
```

Reinstall the package in development mode.

---

**Best Practices**:
1. Test both success and failure cases
2. Use the Inspector for quick manual testing
3. Write automated tests for CI/CD
4. Measure response times
5. Test with diverse input data
6. Mock external APIs for unit tests
7. Document any flaky tests
8. Keep tests fast (< 10s total)

