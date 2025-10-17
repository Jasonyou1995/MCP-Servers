# Documentation Index

Complete documentation for the Python MCP Weather Server.

## Quick Navigation

### Getting Started

1. **[README.md](README.md)** - Main project documentation
   - Overview of features
   - Installation instructions
   - Basic usage
   - Architecture overview

2. **[QUICK_START.md](QUICK_START.md)** - Get up and running fast
   - Prerequisites
   - Installation steps
   - First tool test
   - Common issues

### Development

3. **[INSPECTOR_GUIDE.md](INSPECTOR_GUIDE.md)** - Using the MCP Inspector
   - What is the Inspector
   - How to start it
   - Testing tools interactively
   - Debugging techniques
   - Development workflow

### Integration

4. **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Connect with AI tools
   - Claude Desktop setup
   - VS Code with GitHub Copilot
   - Cursor IDE configuration
   - Windsurf integration
   - Cline setup
   - Zed Editor configuration
   - Continue integration
   - Troubleshooting

## Documentation by Task

### I want to...

#### Install and run the server
→ Start with [QUICK_START.md](QUICK_START.md)

#### Test the server locally
→ See [INSPECTOR_GUIDE.md](INSPECTOR_GUIDE.md)

#### Integrate with my IDE
→ Follow [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)

#### Understand the architecture
→ Read the Architecture section in [README.md](README.md)

#### Modify the server code
→ Review [README.md](README.md) and the source code comments in `server.py`

#### Debug issues
→ Check Troubleshooting sections in each guide

#### Deploy to production
→ See the Usage section in [README.md](README.md)

## File Structure

```
2_mcp-weather-server-py/
├── server.py                   # Main server implementation
├── pyproject.toml              # Python project configuration
├── .gitignore                  # Git ignore rules
├── README.md                   # Main documentation
├── QUICK_START.md              # Quick start guide
├── INSPECTOR_GUIDE.md          # Inspector usage guide
├── INTEGRATION_GUIDE.md        # IDE integration guide
└── DOCUMENTATION_INDEX.md      # This file
```

## Key Concepts

### MCP (Model Context Protocol)

A standard protocol for connecting AI applications to data sources and tools. Read more at [modelcontextprotocol.io](https://modelcontextprotocol.io).

### Tools

Functions that AI assistants can call to perform actions or retrieve data. This server provides:
- **get-weather**: Current weather for a city
- **get-forecast**: 7-day forecast for a city

### Stdio Transport

Communication method using standard input/output streams. This is the default and most common transport for MCP servers.

### FastMCP

A Python framework for building MCP servers quickly using decorators. Part of the official MCP Python SDK.

## API Reference

### Tools

#### get-weather

```python
async def get_weather(city: str) -> dict[str, Any]
```

**Parameters:**
- `city` (string): Name of the city

**Returns:**
- Dictionary with current weather data from Open-Meteo API

**Error Handling:**
- Returns error dictionary if city not found
- Returns error dictionary if API request fails

#### get-forecast

```python
async def get_forecast(city: str) -> dict[str, Any]
```

**Parameters:**
- `city` (string): Name of the city

**Returns:**
- Dictionary with 7-day forecast data from Open-Meteo API

**Error Handling:**
- Returns error dictionary if city not found
- Returns error dictionary if API request fails

### Helper Functions

#### fetch_city_coordinates

```python
async def fetch_city_coordinates(city: str) -> dict[str, Any] | None
```

Geocodes a city name to coordinates using Open-Meteo Geocoding API.

#### fetch_current_weather

```python
async def fetch_current_weather(latitude: float, longitude: float) -> dict[str, Any]
```

Retrieves current weather data for given coordinates.

#### fetch_7day_forecast

```python
async def fetch_7day_forecast(latitude: float, longitude: float) -> dict[str, Any]
```

Retrieves 7-day forecast data for given coordinates.

## External Resources

### Official Documentation

- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- [Open-Meteo API](https://open-meteo.com/en/docs)

### Community

- [MCP Discord](https://discord.gg/mcp)
- [MCP GitHub Discussions](https://github.com/modelcontextprotocol/specification/discussions)

### Related Projects

- [TypeScript Weather Server](../1_mcp-weather-server-ts/README.md) - TypeScript version of this server
- [Other MCP Servers](https://github.com/modelcontextprotocol/servers) - Collection of MCP server examples

## Version History

### 1.0.0 (Current)

- Initial Python implementation
- Two tools: get-weather and get-forecast
- Open-Meteo API integration
- Comprehensive documentation
- MCP Inspector support

## Contributing

When contributing:

1. Follow Python PEP 8 style guidelines
2. Add type hints to all functions
3. Write docstrings for all public functions
4. Update documentation for any API changes
5. Test with MCP Inspector before submitting

## Support

If you encounter issues:

1. Check the Troubleshooting sections in the guides
2. Review the [FAQ](#faq) below
3. Search existing GitHub issues
4. Create a new issue with detailed information

## FAQ

### Why Python instead of TypeScript?

Both implementations are provided. Python offers simpler syntax and is familiar to many developers, while TypeScript provides strong typing and is the original MCP SDK language.

### Do I need an API key for Open-Meteo?

No, Open-Meteo is free and doesn't require an API key for basic usage.

### Can I add more tools?

Yes! Use the `@mcp.tool()` decorator to add new tools. See examples in `server.py`.

### How do I update the server?

Pull the latest changes and reinstall:
```bash
git pull
uv pip install -e .
```

### Does this work offline?

No, the server requires internet access to call the Open-Meteo API.

### Can I customize the weather data?

Yes, modify the API URLs in the fetch functions to include different parameters. See [Open-Meteo API docs](https://open-meteo.com/en/docs).

## License

ISC License - See project root for details.

---

**Last Updated**: October 2025  
**MCP SDK Version**: 1.1.4+  
**Python Version**: 3.10+

