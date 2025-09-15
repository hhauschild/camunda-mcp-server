# MCP Protocol and Communication

## Protocol Overview

The Camunda MCP Server uses the **stdio (Standard Input/Output) protocol** for communication with AI assistants. This is the standard way MCP servers communicate and is supported by:

- **VS Code Copilot** with MCP support
- **Claude Desktop**
- **Other MCP-compatible clients**

## How stdio Protocol Works

### Communication Flow
1. **AI Assistant** launches the MCP server as a child process
2. **Server** communicates via stdin/stdout (no network ports)
3. **JSON-RPC messages** are exchanged over these streams
4. **Tools are called** by the AI assistant when needed

### Benefits of stdio Protocol
- ✅ **Security**: No network exposure, local process communication only
- ✅ **Simplicity**: No port management or firewall configuration  
- ✅ **Reliability**: Direct process communication, no network issues
- ✅ **Standard**: Official MCP protocol specification

## Server Configuration

### VS Code Copilot Configuration
```json
{
  "github.copilot.mcp.servers": {
    "camunda-mcp-server": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

The AI assistant will:
1. Start the server process: `python -m src.server`
2. Connect to stdin/stdout streams
3. Send JSON-RPC messages when tools are needed

### Claude Desktop Configuration  
```json
{
  "mcpServers": {
    "camunda-mcp-server": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/camunda_mcp_server"
    }
  }
}
```

### Docker Configuration
```json
{
  "github.copilot.mcp.servers": {
    "camunda-mcp-server": {
      "command": "docker",
      "args": ["exec", "-i", "camunda-mcp-server", "python", "-m", "src.server"]
    }
  }
}
```

## Technical Implementation

### Server Entry Point
```python
# src/server.py
if __name__ == "__main__":
    logger.info("Starting Camunda MCP Server with stdio transport")
    mcp.run()  # FastMCP handles stdio automatically
```

### Message Flow Example
1. **User asks**: "Show me all my Camunda tasks"
2. **AI Assistant** sends JSON-RPC message via stdin:
   ```json
   {
     "jsonrpc": "2.0",
     "id": 1,
     "method": "tools/call",
     "params": {
       "name": "list_tasks",
       "arguments": {}
     }
   }
   ```
3. **MCP Server** processes request and responds via stdout:
   ```json
   {
     "jsonrpc": "2.0",
     "id": 1,
     "result": {
       "content": [
         {
           "type": "text",
           "text": "Found 3 task(s):\n\nTask ID: abc-123..."
         }
       ]
     }
   }
   ```

## No Network Ports Required

Unlike web servers, MCP servers don't need:
- ❌ Port configuration
- ❌ Firewall rules  
- ❌ Network access
- ❌ HTTP endpoints

Everything happens through **process communication** using stdin/stdout streams.

## Debugging stdio Communication

### Testing Server Directly
```bash
# Run server and test stdio
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python -m src.server
```

### Logging
The server logs to stderr (separate from stdout communication):
```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr  # Important: logs go to stderr, not stdout
)
```

### Docker stdio
Docker containers support stdio communication:
```bash
# Interactive stdio with Docker
docker run -i camunda-mcp-server python -m src.server
```

## Troubleshooting

### Server Not Responding
- Check if server starts: `python -m src.server`
- Verify no stdout pollution (only JSON-RPC messages)
- Check stderr logs for errors

### AI Assistant Can't Connect  
- Verify command path in configuration
- Check working directory is correct
- Ensure Python environment has all dependencies

### Communication Issues
- Server must only write JSON-RPC to stdout
- All logging/debug info goes to stderr
- Check for buffer flushing issues

The stdio protocol is designed to be simple and reliable for local AI assistant integration!