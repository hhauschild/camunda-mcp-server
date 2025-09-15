# Integrating Camunda MCP Server with VS Code Copilot

This guide explains how to integrate your Camunda MCP server with VS Code Copilot to enable AI-powered interaction with your Camunda workflow engine.

## Prerequisites

1. **VS Code with GitHub Copilot Extension**: Ensure you have VS Code with the official GitHub Copilot extension installed
2. **MCP Support**: Your VS Code environment needs to support MCP (Model Context Protocol)
3. **Working Camunda MCP Server**: The server we just built should be ready to run

## Configuration Methods

### Method 1: VS Code Settings (Recommended)

1. **Open VS Code Settings**:
   - Press `Ctrl+,` (Windows) or `Cmd+,` (Mac)
   - Or go to `File > Preferences > Settings`

2. **Navigate to MCP Settings**:
   - Search for "MCP" in the settings search bar
   - Look for GitHub Copilot MCP settings

3. **Add MCP Server Configuration**:
   ```json
   {
     "github.copilot.mcp.servers": {
       "camunda-mcp-server": {
         "command": "C:/Users/hhaus/AppData/Local/Programs/Python/Python312/python.exe",
         "args": ["-m", "src.server"],
         "cwd": "C:\\code\\pythia\\camunda_mcp_server",
         "env": {
           "CAMUNDA_URL": "http://localhost:8080/engine-rest",
           "CAMUNDA_USERNAME": "demo", 
           "CAMUNDA_PASSWORD": "demo",
           "CAMUNDA_AUTH_TYPE": "basic"
         }
       }
     }
   }
   ```

### Method 2: Workspace Settings

1. **Create or Edit `.vscode/settings.json`** in your project root:
   ```json
   {
     "github.copilot.mcp.servers": {
       "camunda-mcp-server": {
         "command": "python",
         "args": ["-m", "src.server"],
         "cwd": "${workspaceFolder}",
         "env": {
           "CAMUNDA_URL": "http://localhost:8080/engine-rest",
           "CAMUNDA_USERNAME": "demo",
           "CAMUNDA_PASSWORD": "demo", 
           "CAMUNDA_AUTH_TYPE": "basic"
         }
       }
     }
   }
   ```

### Method 3: Using .env File (Secure)

If you prefer to keep credentials in a `.env` file:

1. **Create your `.env` file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file** with your actual Camunda credentials:
   ```env
   CAMUNDA_URL=http://your-camunda-server:8080/engine-rest
   CAMUNDA_USERNAME=your-username
   CAMUNDA_PASSWORD=your-password
   CAMUNDA_AUTH_TYPE=basic
   ```

3. **Configure VS Code settings** without credentials:
   ```json
   {
     "github.copilot.mcp.servers": {
       "camunda-mcp-server": {
         "command": "python",
         "args": ["-m", "src.server"],
         "cwd": "C:\\code\\pythia\\camunda_mcp_server"
       }
     }
   }
   ```

## Testing the Integration

Once configured, test the integration:

1. **Restart VS Code** to load the new MCP configuration

2. **Open GitHub Copilot Chat** (`Ctrl+Shift+I` or use the chat icon)

3. **Test with Camunda queries**:
   ```
   @copilot Show me all my Camunda tasks
   @copilot List tasks assigned to john.doe
   @copilot Complete task ABC-123 with result approved
   @copilot What process instances are currently running?
   ```

## Available Commands

Once integrated, you can use these natural language commands with Copilot:

### Task Management
- "Show me all my tasks"
- "List tasks assigned to [username]"  
- "Get details for task [task-id]"
- "Complete task [task-id] with [variables]"
- "Create a new task called [name]"

### Process Management  
- "List all running process instances"
- "Show process instances for [process-key]"
- "Get process definitions"

### Comments
- "Add comment to task [task-id]: [comment]"
- "Show comments for task [task-id]"

## Troubleshooting

### Server Not Starting
- Verify Python path in configuration
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Ensure the working directory is correct

### Authentication Issues
- Verify Camunda server URL and credentials
- Test connection: `python test_server_startup.py`
- Check Camunda server is accessible

### MCP Not Recognized
- Ensure you have the latest GitHub Copilot extension
- Check VS Code version supports MCP
- Look for MCP-related settings in VS Code preferences

### Connection Timeout
- Verify Camunda server is running
- Check network connectivity
- Increase timeout in client configuration if needed

## Security Considerations

1. **Never commit credentials** to version control
2. **Use environment variables** for sensitive data
3. **Restrict network access** to Camunda server if possible  
4. **Use HTTPS** for production Camunda servers
5. **Consider OAuth** instead of basic authentication

## Advanced Configuration

### Custom Tool Descriptions
You can customize how tools appear to Copilot by modifying the tool descriptions in `src/server.py`.

### Adding New Tools
To extend functionality:
1. Add new tool functions in `src/server.py`
2. Implement corresponding Camunda client methods
3. Add tests for new functionality
4. Restart VS Code to reload MCP configuration

## Support

If you encounter issues:
1. Check VS Code Developer Console for errors
2. Review MCP server logs
3. Test server independently: `python -m src.server`
4. Verify Camunda connectivity: `python test_server_startup.py`