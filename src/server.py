#!/usr/bin/env python3
"""
MCP Server for Camunda 7.18 Integration

This server provides Model Context Protocol tools for interacting 
with Camunda workflow engine.
"""

import logging
from typing import Optional, Dict, Any

from mcp.server.fastmcp import FastMCP

try:
    from .camunda.client import CamundaClient
except ImportError:
    # When running as a script, relative imports don't work
    import sys
    import os
    # Add the src directory to path
    src_dir = os.path.dirname(os.path.abspath(__file__))
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    from camunda.client import CamundaClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("camunda-mcp-server")

# Create MCP server
mcp = FastMCP("camunda-mcp-server")

# Initialize Camunda client
camunda_client = CamundaClient()

logger.info("Camunda MCP Server initialized with all tools")


# Task Management Tools
@mcp.tool()
def list_tasks(
    assignee: Optional[str] = None,
    process_definition_key: Optional[str] = None
) -> str:
    """
    List tasks from Camunda, optionally filtered by assignee or process.
    
    Args:
        assignee: Filter tasks by assignee (username)
        process_definition_key: Filter tasks by process definition key
        
    Returns:
        String representation of tasks with details
    """
    try:
        logger.info(
            f"Listing tasks - assignee: {assignee}, "
            f"process: {process_definition_key}"
        )
        
        tasks = camunda_client.get_tasks(
            assignee=assignee,
            process_definition_key=process_definition_key
        )
        
        if not tasks:
            return "No tasks found matching the specified criteria."
        
        # Format tasks for display
        task_list = []
        for task in tasks:
            task_info = [
                f"Task ID: {task.id}",
                f"Name: {task.name or 'Unnamed'}",
                f"Assignee: {task.assignee or 'Unassigned'}",
                f"Created: {task.created or 'Unknown'}",
                f"Due: {task.due or 'No due date'}",
                f"Process Instance: {task.process_instance_id or 'N/A'}",
                f"Description: {task.description or 'No description'}"
            ]
            if task.priority is not None:
                task_info.append(f"Priority: {task.priority}")
            
            task_list.append("\n".join(task_info))
        
        return f"Found {len(tasks)} task(s):\n\n" + "\n\n---\n\n".join(task_list)
        
    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        return f"Error retrieving tasks: {str(e)}"


@mcp.tool()
def get_task_details(task_id: str) -> str:
    """
    Get detailed information for a specific task.
    
    Args:
        task_id: The ID of the task to retrieve
        
    Returns:
        Detailed task information
    """
    try:
        logger.info(f"Getting task details for: {task_id}")
        
        task = camunda_client.get_task(task_id)
        
        details = [
            f"Task Details for {task_id}:",
            f"Name: {task.name or 'Unnamed'}",
            f"Assignee: {task.assignee or 'Unassigned'}",
            f"Owner: {task.owner or 'No owner'}",
            f"Created: {task.created or 'Unknown'}",
            f"Due Date: {task.due or 'No due date'}",
            f"Priority: {task.priority if task.priority is not None else 'Normal'}",
            f"Process Instance ID: {task.process_instance_id or 'N/A'}",
            f"Process Definition ID: {task.process_definition_id or 'N/A'}",
            f"Task Definition Key: {task.task_definition_key or 'N/A'}",
            f"Description: {task.description or 'No description'}",
            f"Suspended: {'Yes' if task.suspended else 'No'}",
            f"Form Key: {task.form_key or 'No form'}"
        ]
        
        if task.delegation_state:
            details.append(f"Delegation State: {task.delegation_state}")
        
        return "\n".join(details)
        
    except Exception as e:
        logger.error(f"Error getting task details: {e}")
        return f"Error retrieving task details: {str(e)}"


@mcp.tool()
def complete_task(
    task_id: str,
    variables: Optional[Dict[str, Any]] = None
) -> str:
    """
    Complete a Camunda task with optional variables.
    
    Args:
        task_id: The ID of the task to complete
        variables: Optional variables to set when completing the task
        
    Returns:
        Confirmation of task completion
    """
    try:
        logger.info(f"Completing task: {task_id}")
        
        # Get task details first to show what we're completing
        task = camunda_client.get_task(task_id)
        
        # Complete the task
        camunda_client.complete_task(task_id, variables)
        
        result_text = "Task completed successfully!\n\n"
        result_text += f"Task ID: {task_id}\n"
        result_text += f"Task Name: {task.name or 'Unnamed'}\n"
        result_text += f"Assignee: {task.assignee or 'Unassigned'}"
        
        if variables:
            result_text += "\n\nVariables set:"
            for key, value in variables.items():
                result_text += f"\n- {key}: {value}"
        
        return result_text
        
    except Exception as e:
        logger.error(f"Error completing task: {e}")
        return f"Error completing task: {str(e)}"


@mcp.tool()  
def create_task(
    name: str,
    assignee: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[int] = None
) -> str:
    """
    Create a new standalone task in Camunda.
    
    Args:
        name: Name of the new task
        assignee: Optional assignee for the task
        description: Optional description for the task  
        priority: Optional priority level (integer)
        
    Returns:
        Details of the created task
    """
    try:
        logger.info(f"Creating new task: {name}")
        
        task_data = {"name": name}
        
        if assignee:
            task_data["assignee"] = assignee
        if description:
            task_data["description"] = description
        if priority is not None:
            task_data["priority"] = str(priority)
        
        task = camunda_client.create_task(task_data)
        
        result_text = "Task created successfully!\n\n"
        result_text += f"Task ID: {task.id}\n"
        result_text += f"Name: {task.name}\n"
        result_text += f"Assignee: {task.assignee or 'Unassigned'}\n"
        result_text += f"Description: {task.description or 'No description'}\n"
        result_text += (
            f"Priority: {task.priority if task.priority is not None else 'Normal'}"
        )
        
        return result_text
        
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return f"Error creating task: {str(e)}"


# Process Management Tools
@mcp.tool()
def list_process_instances(
    process_definition_key: Optional[str] = None,
    business_key: Optional[str] = None
) -> str:
    """
    List process instances from Camunda.
    
    Args:
        process_definition_key: Filter by process definition key
        business_key: Filter by business key
        
    Returns:
        List of process instances
    """
    try:
        logger.info("Listing process instances")
        
        filters = {}
        if business_key:
            filters["businessKey"] = business_key
        
        instances = camunda_client.get_process_instances(
            process_definition_key=process_definition_key,
            **filters
        )
        
        if not instances:
            return "No process instances found matching the criteria."
        
        # Format instances for display
        instance_list = []
        for instance in instances:
            instance_info = [
                f"Instance ID: {instance.id}",
                f"Definition ID: {instance.definition_id}",
                f"Business Key: {instance.business_key or 'None'}",
                f"Status: {'Ended' if instance.ended else 'Active'}",
                f"Suspended: {'Yes' if instance.suspended else 'No'}"
            ]
            
            if instance.tenant_id:
                instance_info.append(f"Tenant: {instance.tenant_id}")
            
            instance_list.append("\n".join(instance_info))
        
        return (
            f"Found {len(instances)} process instance(s):\n\n" +
            "\n\n---\n\n".join(instance_list)
        )
        
    except Exception as e:
        logger.error(f"Error listing process instances: {e}")
        return f"Error retrieving process instances: {str(e)}"


@mcp.tool()
def list_process_definitions() -> str:
    """
    List available process definitions from Camunda.
    
    Returns:
        List of process definitions with their details
    """
    try:
        logger.info("Listing process definitions")
        
        definitions = camunda_client.get_process_definitions()
        
        if not definitions:
            return "No process definitions found."
        
        # Format definitions for display  
        definition_list = []
        for definition in definitions:
            def_info = [
                f"ID: {definition.get('id', 'Unknown')}",
                f"Key: {definition.get('key', 'Unknown')}",
                f"Name: {definition.get('name', 'Unnamed')}",
                f"Version: {definition.get('version', 'Unknown')}",
                f"Deployment ID: {definition.get('deploymentId', 'Unknown')}",
                f"Resource Name: {definition.get('resource', 'Unknown')}"
            ]
            
            if definition.get("suspended"):
                def_info.append("Status: Suspended")
            else:
                def_info.append("Status: Active")
            
            if definition.get("tenantId"):
                def_info.append(f"Tenant: {definition['tenantId']}")
            
            definition_list.append("\n".join(def_info))
        
        return (
            f"Found {len(definitions)} process definition(s):\n\n" +
            "\n\n---\n\n".join(definition_list)
        )
        
    except Exception as e:
        logger.error(f"Error listing process definitions: {e}")
        return f"Error retrieving process definitions: {str(e)}"


# Comment Management Tools
@mcp.tool()
def get_task_comments(task_id: str) -> str:
    """
    Get all comments for a specific task.
    
    Args:
        task_id: The ID of the task to get comments for
        
    Returns:
        List of comments for the task
    """
    try:
        logger.info(f"Getting comments for task: {task_id}")
        
        comments = camunda_client.get_task_comments(task_id)
        
        if not comments:
            return f"No comments found for task {task_id}."
        
        # Format comments for display
        comment_list = []
        for comment in comments:
            comment_info = [
                f"Comment ID: {comment.id}",
                f"Author: {comment.user_id or 'System'}",
                f"Time: {comment.time or 'Unknown'}",
                f"Message: {comment.message}"
            ]
            
            comment_list.append("\n".join(comment_info))
        
        return (
            f"Found {len(comments)} comment(s) for task {task_id}:\n\n" +
            "\n\n---\n\n".join(comment_list)
        )
        
    except Exception as e:
        logger.error(f"Error getting task comments: {e}")
        return f"Error retrieving comments: {str(e)}"


@mcp.tool()
def add_task_comment(task_id: str, message: str) -> str:
    """
    Add a comment to a specific task.
    
    Args:
        task_id: The ID of the task to add a comment to
        message: The comment message text
        
    Returns:
        Confirmation of comment addition with details
    """
    try:
        logger.info(f"Adding comment to task: {task_id}")
        
        comment = camunda_client.add_task_comment(task_id, message)
        
        result_text = "Comment added successfully!\n\n"
        result_text += f"Comment ID: {comment.id}\n"
        result_text += f"Task ID: {task_id}\n"
        result_text += f"Author: {comment.user_id or 'System'}\n"
        result_text += f"Time: {comment.time or 'Just now'}\n"
        result_text += f"Message: {comment.message}"
        
        return result_text
        
    except Exception as e:
        logger.error(f"Error adding task comment: {e}")
        return f"Error adding comment: {str(e)}"


# Main entry point for MCP stdio protocol
if __name__ == "__main__":
    logger.info("Starting Camunda MCP Server with stdio transport")
    
    # FastMCP automatically handles stdio protocol when run as main
    mcp.run()
