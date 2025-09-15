# Camunda MCP Server

A Model Context Protocol (MCP) server that enables AI assistants like VS Code Copilot and Claude Desktop to interact with your Camunda workflow engine.

> ⚠️ **Early Stage Work in Progress**: This is an early-stage implementation. So far, it has only been tested with **Camunda 7.18** and **GitHub Copilot**. Feedback and contributions are welcome.


## Features

🤖 **AI Assistant Integration**: Talk to your Camunda server using natural language  
📋 **Task Management**: List, view, create, and complete tasks  
💬 **Comments**: Add and read task comments  
⚙️ **Process Management**: Query process instances and definitions  
🐳 **Docker Ready**: Run with Docker or Docker Compose  


## Available Tools

### Task Management  
- **list_tasks**: Get user task lists with optional filtering (assignee, process, etc.)
- **get_task_details**: Retrieve comprehensive task information including variables
- **complete_task**: Complete tasks with optional variables and comments
- **create_task**: Create standalone tasks (if workflow supports it)

### Comments  
- **add_task_comment**: Add comments to existing tasks
- **get_task_comments**: Retrieve comment history for tasks

### Process Management
- **list_process_instances**: Query running/completed process instances
- **list_process_definitions**: Retrieve BPMN process definitions and metadata

## Quick Examples

Once configured, you can ask your AI assistant:

- *"Show me all my Camunda tasks"*
- *"Complete task ABC-123 with result approved"*  
- *"List running process instances"*
- *"Add comment to task XYZ: Review completed"*
- *"Create a new task called 'Review Document'"*

## Getting Started

### Option 1: Docker

1. **Quick Start**
   ```bash
   git clone https://github.com/hhauschild/camunda-mcp-server.git
   cd camunda_mcp_server
   
   # Windows
   start-docker.bat
   
   # Linux/Mac
   ./start-docker.sh
   ```

2. **Manual Docker Setup**
   ```bash
   # Configure environment
   cp .env.example .env
   # Edit .env with your Camunda server details
   
   # Run with Docker Compose
   docker-compose up -d
   ```

### Option 2: Python 

1. **Clone and Setup**
   ```bash
   git clone https://github.com/hhauschild/camunda-mcp-server.git
   cd camunda_mcp_server
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   copy .env.example .env
   # Edit .env with your Camunda server details
   ```

3. **Run MCP Server**
   ```bash
   python -m src.server
   ```

4. **Configure AI Assistant**
   
   The MCP server uses the **stdio protocol** (standard input/output) for communication - no network ports needed!
   
   **For VS Code Copilot:**
   - edit mcp.json in the .vscode folder
   ```
		"camunda-mcp-server": {
			"type": "stdio",
			"command": "/path/to/python.exe",
			"args": [
				"-m",
				"src.server"
			],
			"cwd": "<base-path>/camunda_mcp_server",
			"env": {
				"CAMUNDA_URL": "http://<camunda-server>/engine-rest",
				"CAMUNDA_USERNAME": "demo",
				"CAMUNDA_PASSWORD": "demo",
				"CAMUNDA_AUTH_TYPE": "basic"
			}
		}
   
   ```
   
   **For Claude Desktop:**
   - Add MCP server configuration from `examples/claude_desktop_config.json`
   - Update paths and credentials as needed
   
   📚 **Learn more**: See `docs/mcp_protocol.md` for technical details about stdio communication

## Configuration

Set up your Camunda connection using environment variables:

```bash
CAMUNDA_URL=http://localhost:8080/engine-rest
CAMUNDA_USERNAME=demo  
CAMUNDA_PASSWORD=demo
CAMUNDA_AUTH_TYPE=basic  # basic, oauth, none
LOG_LEVEL=INFO
```

## Troubleshooting

### Common Issues

- **Connection errors**: Verify Camunda URL and credentials
- **MCP server not found**: Check Python path in AI assistant configuration  
- **Permission denied**: Ensure service account has necessary Camunda permissions
- **Tools not working**: Restart your AI assistant after configuration changes

### Getting Help

- 📖 Check the [documentation](docs/) for detailed guides
- 🐛 [Report bugs](../../issues/new?template=bug_report.yml) with issue templates
- 💡 [Request features](../../issues/new?template=feature_request.yml) for new functionality
- 💬 Join discussions for community support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:
1. Check the [documentation](docs/) for common solutions
2. Search existing [GitHub Issues](../../issues)
3. Create a new issue with detailed information about your problem

## Acknowledgments

- Built with the [Model Context Protocol](https://modelcontextprotocol.io/) framework
- Integrates with [Camunda 7.18](https://camunda.com/) workflow engine
- Supports [VS Code Copilot](https://code.visualstudio.com/) and (hopefully) [Claude Desktop](https://claude.ai/)
