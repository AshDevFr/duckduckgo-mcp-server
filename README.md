# DuckDuckGo MCP Server

Node.js server implementing Model Context Protocol (MCP) for DuckDuckGo web search.

## Features

- Web Search using DuckDuckGo.

## API

### Tools

- **search**
    - Search the web using DuckDuckGo.
    - Input: `query` (string)
    - Returns an array of results

## Usage with Claude Desktop
Add this to your `claude_desktop_config.json`:

### UVX

```json
{
  "mcpServers": {
    "duckduckgo": {
      "command": "uvx",
      "args": [
        "ddg-mcp-server"
      ]
    }
  }
}
```

### Docker

```json
{
  "mcpServers": {
    "duckduckgo": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "ashdev/duckduckgo-mcp-server"
      ]
    }
  }
}
```
