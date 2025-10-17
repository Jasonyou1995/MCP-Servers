# Integration Guide

Complete instructions for integrating the Python MCP Weather Server with various AI IDEs and tools.

## Table of Contents

- [Claude Desktop](#claude-desktop)
- [VS Code with GitHub Copilot](#vs-code-with-github-copilot)
- [Cursor IDE](#cursor-ide)
- [Windsurf](#windsurf)
- [Cline](#cline)
- [Zed Editor](#zed-editor)
- [Continue](#continue)

---

## Claude Desktop

### Configuration File Location

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Configuration

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/2_mcp-weather-server-py",
        "run",
        "server.py"
      ]
    }
  }
}
```

### Steps

1. Open the configuration file in your text editor
2. Add the weather server configuration (replace `/absolute/path/to/` with your actual path)
3. Save the file
4. Restart Claude Desktop
5. Look for the hammer icon (🔨) to see available tools
6. Ask Claude: "What's the weather in London?"

---

## VS Code with GitHub Copilot

### Configuration

Add to your VS Code settings (`settings.json`):

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
        "/absolute/path/to/2_mcp-weather-server-py",
        "run",
        "server.py"
      ]
    }
  }
}
```

### Steps

1. Open VS Code Settings (Cmd/Ctrl + ,)
2. Click "Open Settings (JSON)" in the top right
3. Add the configuration above
4. Reload VS Code
5. Open GitHub Copilot Chat
6. Ask: "Get me the weather forecast for Paris"

---

## Cursor IDE

### Configuration File Location

- **macOS/Linux**: `~/.cursor/config.json`
- **Windows**: `%USERPROFILE%\.cursor\config.json`

Or create a workspace-specific config at `.cursor/config.json` in your project root.

### Configuration

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/2_mcp-weather-server-py",
        "run",
        "server.py"
      ]
    }
  }
}
```

### Steps

1. Create or open the config file
2. Add the weather server configuration
3. Save the file
4. Restart Cursor
5. Use Cmd/Ctrl + K to open the AI panel
6. Ask: "What's the weather like in Tokyo?"

---

## Windsurf

### Configuration File Location

- **macOS**: `~/Library/Application Support/Windsurf/windsurf_config.json`
- **Windows**: `%APPDATA%\Windsurf\windsurf_config.json`
- **Linux**: `~/.config/Windsurf/windsurf_config.json`

### Configuration

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/2_mcp-weather-server-py",
        "run",
        "server.py"
      ]
    }
  }
}
```

### Steps

1. Open Windsurf settings
2. Navigate to MCP Servers configuration
3. Add the weather server configuration
4. Restart Windsurf
5. Open the AI assistant
6. Ask: "Get weather forecast for New York"

---

## Cline

### Configuration

Cline uses the VS Code extension model. Add to your VS Code settings:

```json
{
  "cline.mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/2_mcp-weather-server-py",
        "run",
        "server.py"
      ]
    }
  }
}
```

### Steps

1. Install the Cline extension in VS Code
2. Open VS Code Settings (JSON)
3. Add the configuration above
4. Reload VS Code
5. Open Cline panel
6. Ask: "What's the weather in Berlin?"

---

## Zed Editor

### Configuration File Location

- **macOS**: `~/.config/zed/settings.json`
- **Linux**: `~/.config/zed/settings.json`

### Configuration

```json
{
  "context_servers": {
    "weather": {
      "command": {
        "path": "uv",
        "args": [
          "--directory",
          "/absolute/path/to/2_mcp-weather-server-py",
          "run",
          "server.py"
        ]
      }
    }
  }
}
```

### Steps

1. Open Zed settings
2. Add the context server configuration
3. Restart Zed
4. Open AI assistant panel
5. Ask: "Show me the weather in San Francisco"

---

## Continue

### Configuration

Continue uses a `.continue/config.json` file in your project root:

```json
{
  "mcpServers": [
    {
      "name": "weather",
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/2_mcp-weather-server-py",
        "run",
        "server.py"
      ]
    }
  ]
}
```

### Steps

1. Create `.continue/config.json` in your project
2. Add the configuration above
3. Restart your IDE
4. Open Continue panel
5. Ask: "What's the forecast for Seattle?"

---

## Troubleshooting

### Server Not Starting

1. **Check Python version**:
   ```bash
   python --version
   ```
   Must be 3.10+

2. **Verify uv is installed**:
   ```bash
   uv --version
   ```

3. **Test server manually**:
   ```bash
   cd /path/to/2_mcp-weather-server-py
   uv run server.py
   ```

### Tools Not Appearing

1. **Check configuration path**: Ensure the `--directory` path is absolute and correct
2. **Check logs**: Look for error messages in the IDE's output/console
3. **Restart the IDE**: Some IDEs require a full restart

### Permission Issues

On macOS/Linux, ensure the server.py file is executable:
```bash
chmod +x server.py
```

### Environment Variables

If you need to pass environment variables:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/2_mcp-weather-server-py",
        "run",
        "server.py"
      ],
      "env": {
        "CUSTOM_VAR": "value"
      }
    }
  }
}
```

---

## Testing Your Integration

Once configured, test with these example queries:

1. **Simple weather query**: "What's the weather in London?"
2. **Forecast query**: "Give me the 7-day forecast for Paris"
3. **Multiple cities**: "Compare the weather in New York and Tokyo"
4. **Specific data**: "What's the humidity in Berlin right now?"

The AI assistant should automatically use the weather server tools to answer these questions.

---

## Alternative: Using Python Directly (Without uv)

If you prefer not to use `uv`, you can run with Python directly:

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": [
        "/absolute/path/to/2_mcp-weather-server-py/server.py"
      ]
    }
  }
}
```

Make sure to have dependencies installed:
```bash
pip install mcp httpx
```

