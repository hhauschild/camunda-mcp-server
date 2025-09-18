# Camunda MCP Server Usage Examples

This document provides examples of how to use the Camunda MCP Server with AI assistants.

## Setup

1. **Configure Environment Variables**
   Create a `.env` file in the project root:
   ```bash
   CAMUNDA_URL=http://localhost:8080/engine-rest
   CAMUNDA_USERNAME=demo
   CAMUNDA_PASSWORD=demo
   CAMUNDA_AUTH_TYPE=basic
   LOG_LEVEL=INFO
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Claude Desktop**
   Add the configuration from `claude_desktop_config.json` to your Claude Desktop settings.

## Available Tools

### Task Management

#### List Tasks
```
"Show me all tasks assigned to john.doe"
"List all tasks for the invoice process"
"Get all unassigned tasks"
```

#### Get Task Details
```
"Show me details for task abc-123"
"What information do you have about task def-456?"
```

#### Complete Tasks
```
"Complete task abc-123 with result approved"
"Finish task def-456 and set amount to 1500"
```

#### Create Tasks
```
"Create a new task called 'Review Document' assigned to jane.smith"
"Add a task 'Follow up call' with priority 75"
```

### Process Management

#### List Process Instances
```
"Show me all running invoice processes"
"List process instances with business key ORDER-2024-001"
"Get all active process instances"
```

#### List Process Definitions
```
"What process definitions are available?"
"Show me all deployed processes"
```

#### Start Process Instance
```
"Start a new invoice process"
"Create a process instance for order-processing with business key ORDER-2024-001"
"Start process loan-approval with variables amount=50000 and customer=john.doe"
```

### Comment Management

#### Get Task Comments
```
"Show me all comments for task abc-123"
"What comments are there on task def-456?"
```

#### Add Task Comments
```
"Add a comment to task abc-123: 'Waiting for approval from manager'"
"Comment on task def-456: 'Customer provided additional documentation'"
```

## Example Conversations

### Scenario 1: Daily Task Review
**User**: "Show me all my tasks for today"
**Assistant**: Uses `list_tasks` with your username to show assigned tasks

**User**: "What's the status of task abc-123?"
**Assistant**: Uses `get_task_details` to show complete task information

**User**: "Add a comment that I'm waiting for customer input"
**Assistant**: Uses `add_task_comment` to add the comment

### Scenario 2: Process Monitoring
**User**: "How many invoice processes are currently running?"
**Assistant**: Uses `list_process_instances` with filter for invoice process

**User**: "Show me the details of process instance xyz-789"
**Assistant**: Provides process instance information

### Scenario 3: Starting New Processes
**User**: "I need to start a new invoice process for order ORDER-2024-001"
**Assistant**: Uses `start_process_instance` with process key and business key

**User**: "Start the loan approval process with amount 75000 and customer ID 12345"
**Assistant**: Uses `start_process_instance` with variables for the loan approval

**User**: "What processes can I start?"
**Assistant**: Uses `list_process_definitions` to show available process definitions

### Scenario 4: Task Completion
**User**: "I've approved the expense report in task def-456, mark it complete"
**Assistant**: Uses `complete_task` with appropriate variables

**User**: "Add a comment explaining why I approved it"
**Assistant**: Uses `add_task_comment` to add the explanation

## Error Handling

The MCP server provides helpful error messages:

- **Connection Issues**: "Error connecting to Camunda server at http://localhost:8080"
- **Authentication**: "Authentication failed - check username/password"
- **Not Found**: "Task abc-123 not found"
- **Permission**: "Insufficient permissions to complete this task"

## Tips for AI Interaction

1. **Be Specific**: Include task IDs, usernames, or process keys when known
2. **Natural Language**: Use conversational language - the AI will translate to appropriate tool calls
3. **Context Matters**: Mention what you're trying to accomplish for better assistance
4. **Follow Up**: Ask for details or clarification as needed

## Configuration Examples

### Different Camunda Environments

**Development**:
```json
{
  "env": {
    "CAMUNDA_URL": "http://localhost:8080/engine-rest",
    "CAMUNDA_USERNAME": "demo",
    "CAMUNDA_PASSWORD": "demo"
  }
}
```

**Production** (with OAuth):
```json
{
  "env": {
    "CAMUNDA_URL": "https://camunda.company.com/engine-rest",
    "CAMUNDA_AUTH_TYPE": "oauth",
    "CAMUNDA_CLIENT_ID": "your-client-id",
    "CAMUNDA_CLIENT_SECRET": "your-client-secret"
  }
}
```

### Multiple Camunda Instances
You can configure multiple MCP servers for different Camunda environments:

```json
{
  "mcpServers": {
    "camunda-dev": {
      "command": "python",
      "args": ["-m", "src.server"],
      "env": {
        "CAMUNDA_URL": "http://localhost:8080/engine-rest"
      }
    },
    "camunda-prod": {
      "command": "python", 
      "args": ["-m", "src.server"],
      "env": {
        "CAMUNDA_URL": "https://prod-camunda.company.com/engine-rest"
      }
    }
  }
}
```
