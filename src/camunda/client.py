"""
Camunda REST API Client

Provides a Python client for interacting with Camunda 7.18 REST API.
"""

import os
import logging
from typing import Dict, List, Optional, Any, cast
from dataclasses import dataclass
import requests
from requests.auth import HTTPBasicAuth

from .models import Task, ProcessInstance, Comment

logger = logging.getLogger(__name__)


@dataclass
class CamundaConfig:
    """Configuration for Camunda connection."""
    
    url: str
    username: Optional[str] = None
    password: Optional[str] = None
    auth_type: str = "basic"  # basic, oauth, none
    timeout: int = 30
    
    @classmethod
    def from_environment(cls) -> "CamundaConfig":
        """Create configuration from environment variables."""
        return cls(
            url=os.getenv("CAMUNDA_URL", "http://localhost:8080/engine-rest"),
            username=os.getenv("CAMUNDA_USERNAME"),
            password=os.getenv("CAMUNDA_PASSWORD"),
            auth_type=os.getenv("CAMUNDA_AUTH_TYPE", "basic"),
            timeout=int(os.getenv("CAMUNDA_TIMEOUT", "30"))
        )


class CamundaClient:
    """Client for interacting with Camunda REST API."""
    
    def __init__(self, config: Optional[CamundaConfig] = None):
        """Initialize Camunda client with configuration."""
        self.config = config or CamundaConfig.from_environment()
        self.session = requests.Session()
        
        # Set up authentication
        if self.config.auth_type == "basic" and self.config.username:
            self.session.auth = HTTPBasicAuth(
                self.config.username, 
                self.config.password or ""
            )
        
        logger.info(f"Camunda client initialized for {self.config.url}")
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        **kwargs: Any
    ) -> Any:
        """Make HTTP request to Camunda REST API."""
        url = f"{self.config.url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method, 
                url, 
                timeout=self.config.timeout,
                **kwargs
            )
            response.raise_for_status()
            
            # Handle empty responses
            if response.status_code == 204 or not response.content:
                return {}
            
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Camunda API request failed: {e}")
            raise
    
    # Task Management Methods
    
    def get_tasks(
        self, 
        assignee: Optional[str] = None,
        process_definition_key: Optional[str] = None,
        **filters: Any
    ) -> List[Task]:
        """Get list of tasks with optional filtering."""
        
        params = {}
        if assignee:
            params["assignee"] = assignee
        if process_definition_key:
            params["processDefinitionKey"] = process_definition_key
        params.update(filters)
        
        data = self._make_request("GET", "/task", params=params)
        return [Task.from_dict(task_data) for task_data in data]
    
    def get_task(self, task_id: str) -> Task:
        """Get detailed information for a specific task."""
        data = self._make_request("GET", f"/task/{task_id}")
        return Task.from_dict(data)
    
    def complete_task(
        self, 
        task_id: str, 
        variables: Optional[Dict[str, Any]] = None
    ) -> None:
        """Complete a task with optional variables."""
        
        payload = {}
        if variables:
            payload["variables"] = {
                key: {"value": value} for key, value in variables.items()
            }
        
        self._make_request("POST", f"/task/{task_id}/complete", json=payload)
        logger.info(f"Task {task_id} completed successfully")
    
    def create_task(self, task_data: Dict[str, Any]) -> Task:
        """Create a new task."""
        data = self._make_request("POST", "/task/create", json=task_data)
        return Task.from_dict(data)
    
    # Comment Management Methods
    
    def get_task_comments(self, task_id: str) -> List[Comment]:
        """Get comments for a specific task."""
        data = self._make_request("GET", f"/task/{task_id}/comment")
        return [Comment.from_dict(comment_data) for comment_data in data]
    
    def add_task_comment(self, task_id: str, message: str) -> Comment:
        """Add a comment to a task."""
        payload = {"message": message}
        data = self._make_request("POST", f"/task/{task_id}/comment", json=payload)
        return Comment.from_dict(data)
    
    # Process Management Methods
    
    def get_process_instances(
        self, 
        process_definition_key: Optional[str] = None,
        **filters: Any
    ) -> List[ProcessInstance]:
        """Get list of process instances."""
        
        params = {}
        if process_definition_key:
            params["processDefinitionKey"] = process_definition_key
        params.update(filters)
        
        data = self._make_request("GET", "/process-instance", params=params)
        return [ProcessInstance.from_dict(pi_data) for pi_data in data]
    
    def get_process_definitions(self) -> List[Dict[str, Any]]:
        """Get list of process definitions."""
        data = self._make_request("GET", "/process-definition")
        return cast(List[Dict[str, Any]], data)
    
    def health_check(self) -> bool:
        """Check if Camunda server is accessible."""
        try:
            self._make_request("GET", "/engine")
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
