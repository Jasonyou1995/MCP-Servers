# MCP Weather Server Integration Guide

This guide shows you how to integrate the MCP Weather Server with various IDEs and tools that support the Model Context Protocol.

## Table of Contents

- [VS Code with GitHub Copilot](#vs-code-with-github-copilot)
- [Claude Desktop](#claude-desktop)
- [Cursor IDE](#cursor-ide)
- [Windsurf](#windsurf)
- [Cline (VS Code Extension)](#cline-vs-code-extension)
- [Zed Editor](#zed-editor)
- [Continue (VS Code/JetBrains)](#continue-vs-codejetbrains)
- [Configuration Files Reference](#configuration-files-reference)

---

## VS Code with GitHub Copilot

### Prerequisites
- VS Code with GitHub Copilot extension installed
- MCP support enabled in VS Code (latest version)

### Step 1: Build Your Server
```bash
cd 1_mcp-weather-server
npm install
npm run build
```

### Step 2: Register the Server

1. **Open Command Palette**: `Cmd/Ctrl + Shift + P`
2. **Type**: `MCP: Add Server`
3. **Choose**: "Local server using stdio"
4. **Enter Command**: `npx -y tsx main.ts`
5. **Name**: `my-weather-server`
6. **Setup Type**: Local setup

This creates a `.vscode/mcp.json` file in your project:

```json
{
  "inputs": [],
  "servers": {
    "my-weather-server": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "tsx",
        "/Users/your-username/Documents/GitHub/MCP-Servers/1_mcp-weather-server/main.ts"
      ]
    }
  }
}
```

**Important**: Replace `/Users/your-username/Documents/GitHub/MCP-Servers/` with your actual path!

### Step 3: Start and Test

1. **Start the server**: Click the "Start" button next to your server name in the MCP panel
2. **Verify**: You should see "Running" status with a green indicator
3. **Switch to Agent Mode**: Click the Copilot sidebar → "Agent Mode"
4. **Ask**: "What's the weather like in Tokyo?"

GitHub Copilot will ask permission to use your weather tool - click **"Continue"** to proceed.

### Step 4: Example Usage

Try these prompts in GitHub Copilot Agent Mode:

```
You: What's the weather in London?
→ Copilot uses get-weather tool

You: Give me a 7-day forecast for Paris
→ Copilot uses get-forecast tool

You: Compare the weather in Tokyo and New York
→ Copilot uses get-weather twice and compares
```

### Troubleshooting VS Code

**Server won't start?**
- Check the path in `.vscode/mcp.json` is absolute and correct
- Verify `tsx` is available: `npm install -g tsx`
- Check VS Code Output panel for MCP logs

**Tool not appearing?**
- Restart VS Code
- Check MCP panel shows server as "Running"
- Try stopping and starting the server

**Permission denied?**
- Make sure you clicked "Continue" when Copilot asks for permission
- Check MCP settings in VS Code preferences

---

## Claude Desktop

### Step 1: Build Your Server
```bash
npm install
npm run build
```

### Step 2: Locate Configuration File

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**Linux**: `~/.config/Claude/claude_desktop_config.json`

### Step 3: Add Server Configuration

Edit the configuration file:

```json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": [
        "/Users/your-username/Documents/GitHub/MCP-Servers/1_mcp-weather-server/dist/main.js"
      ]
    }
  }
}
```

### Step 4: Restart Claude Desktop

Completely quit and restart Claude Desktop for changes to take effect.

### Step 5: Test Integration

In Claude, try:
```
You: What's the current weather in Tokyo?
Claude: [Uses get-weather tool and provides weather information]

You: Show me the forecast for the next week in Paris
Claude: [Uses get-forecast tool and presents 7-day forecast]
```

### Troubleshooting Claude Desktop

**Tools not showing up?**
- Check JSON syntax is valid (use a JSON validator)
- Ensure paths are absolute
- Look at Claude logs: `~/Library/Logs/Claude/mcp*.log`

**Server crashes?**
- Verify `npm run build` completed successfully
- Test server manually: `node dist/main.js`
- Check Node.js version is 18 or higher

---

## Cursor IDE

Cursor has built-in MCP support similar to VS Code.

### Configuration

1. Open Cursor Settings
2. Navigate to **Features** → **Model Context Protocol**
3. Click **"Add Server"**
4. Use the same configuration as VS Code:

```json
{
  "weather-server": {
    "command": "node",
    "args": [
      "/absolute/path/to/1_mcp-weather-server/dist/main.js"
    ]
  }
}
```

### Usage in Cursor

- Enable Cursor Agent Mode
- Ask: "Check the weather in Singapore"
- Cursor will automatically use available tools

---

## Windsurf

Windsurf supports MCP through its AI assistant.

### Configuration Location

Create or edit: `.windsurf/mcp.json` in your workspace

```json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": [
        "/absolute/path/to/1_mcp-weather-server/dist/main.js"
      ],
      "env": {}
    }
  }
}
```

### Usage

1. Open Windsurf
2. Start the AI assistant
3. Say: "What's the weather in Berlin?"
4. Windsurf AI will use your weather tools

---

## Cline (VS Code Extension)

Cline is a VS Code extension that supports MCP servers.

### Configuration

1. Install Cline extension from VS Code marketplace
2. Open Cline settings
3. Add MCP server configuration:

**Settings Location**: `.vscode/cline_mcp_settings.json`

```json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": [
        "/absolute/path/to/1_mcp-weather-server/dist/main.js"
      ]
    }
  }
}
```

### Usage

- Open Cline chat panel
- Type: "Get weather for Sydney"
- Cline will invoke your weather tools

---

## Zed Editor

Zed has experimental MCP support.

### Configuration

Create or edit: `~/.config/zed/mcp.json`

```json
{
  "servers": {
    "weather": {
      "command": "node",
      "args": [
        "/absolute/path/to/1_mcp-weather-server/dist/main.js"
      ]
    }
  }
}
```

### Enable MCP in Zed

1. Open Zed Settings
2. Search for "MCP"
3. Enable "Model Context Protocol Support"
4. Restart Zed

### Usage

- Use Zed's AI assistant
- Request weather information
- Zed will call your MCP tools

---

## Continue (VS Code/JetBrains)

Continue is an AI coding assistant that supports MCP.

### VS Code Configuration

Add to `.continue/config.json`:

```json
{
  "mcpServers": [
    {
      "name": "weather",
      "command": "node",
      "args": [
        "/absolute/path/to/1_mcp-weather-server/dist/main.js"
      ]
    }
  ]
}
```

### JetBrains Configuration

Similar configuration in JetBrains settings under Continue plugin settings.

### Usage

1. Open Continue panel
2. Type your request
3. Continue will use weather tools when relevant

---

## Configuration Files Reference

### Using TypeScript Source (Development)

Requires `tsx` to be installed globally:

```json
{
  "command": "npx",
  "args": ["-y", "tsx", "/path/to/main.ts"]
}
```

**Pros**: No build step needed  
**Cons**: Slower startup

### Using Compiled JavaScript (Production)

```json
{
  "command": "node",
  "args": ["/path/to/dist/main.js"]
}
```

**Pros**: Faster startup  
**Cons**: Requires build step

### With Environment Variables

```json
{
  "command": "node",
  "args": ["/path/to/dist/main.js"],
  "env": {
    "DEBUG": "true",
    "LOG_LEVEL": "info"
  }
}
```

### Complete Example

```json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": [
        "/Users/jasony/Documents/GitHub/MCP-Servers/1_mcp-weather-server/dist/main.js"
      ],
      "env": {
        "NODE_ENV": "production"
      }
    }
  }
}
```

---

## General Integration Tips

### 🎯 Best Practices

1. **Always use absolute paths** - Relative paths may not work across different tools
2. **Build first** - Run `npm run build` before integrating
3. **Test with Inspector** - Verify tools work with `npm run inspect` before IDE integration
4. **Check logs** - Each tool has its own log location for troubleshooting

### 📝 Path Finding

Get your absolute path:

**macOS/Linux**:
```bash
cd 1_mcp-weather-server
pwd
# Copy this path and append /dist/main.js
```

**Windows**:
```cmd
cd 1_mcp-weather-server
cd
# Copy this path and append \dist\main.js
```

### 🔄 Server Updates

When you update your server:

1. Make changes to `main.ts`
2. Run `npm run build`
3. Restart the MCP server in your IDE
4. No configuration changes needed!

### 🐛 Debugging

If tools aren't working:

1. **Test standalone**: `node dist/main.js` should not crash
2. **Test with inspector**: `npm run inspect` should work
3. **Check IDE logs**: Each tool has MCP logs
4. **Verify paths**: Use absolute paths, check they exist
5. **Permissions**: Ensure the IDE can execute Node.js

---

## Platform-Specific Notes

### macOS

- Use forward slashes: `/Users/username/path/to/file.js`
- Watch for spaces in paths: Use full path or escape spaces
- May need to allow Node.js in Security & Privacy settings

### Windows

- Use forward slashes or escaped backslashes: `C:/Users/username/path/to/file.js`
- Watch for spaces in `Program Files` paths
- May need to run IDE as administrator

### Linux

- Use forward slashes: `/home/username/path/to/file.js`
- Ensure Node.js is in PATH
- Check file permissions: `chmod +x dist/main.js`

---

## Testing Your Integration

After configuration, test with these prompts:

### Basic Test
```
"What's the weather in London?"
```
Expected: Should use `get-weather` tool

### Forecast Test
```
"Show me the 7-day forecast for Tokyo"
```
Expected: Should use `get-forecast` tool

### Error Handling Test
```
"Get weather for InvalidCityXYZ123"
```
Expected: Should show error message about city not found

### Multiple Tools Test
```
"Compare the current weather and forecast for Paris"
```
Expected: Should use both `get-weather` and `get-forecast`

---

## Verification Checklist

- [ ] Server builds successfully (`npm run build`)
- [ ] Server runs standalone (`node dist/main.js`)
- [ ] Inspector shows both tools (`npm run inspect`)
- [ ] Configuration file has correct absolute path
- [ ] IDE/Tool recognizes the server
- [ ] Server starts without errors
- [ ] Tools appear in available tools list
- [ ] Test prompts work correctly
- [ ] Error handling works (invalid city test)

---

## Need Help?

- **Inspector not working?** → See [INSPECTOR_GUIDE.md](INSPECTOR_GUIDE.md)
- **General questions?** → See [README.md](README.md)
- **Quick setup?** → See [QUICK_START.md](QUICK_START.md)

---

**Enjoy your weather-powered AI assistants! ☀️🌧️❄️**

