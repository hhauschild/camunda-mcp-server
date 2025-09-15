"""
Data models for Camunda entities

Defines dataclasses for Camunda REST API responses.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional


@dataclass
class Task:
    """Represents a Camunda task."""
    
    id: str
    name: Optional[str]
    assignee: Optional[str]
    created: Optional[datetime]
    due: Optional[datetime]
    process_instance_id: Optional[str]
    process_definition_id: Optional[str]
    case_instance_id: Optional[str]
    case_definition_id: Optional[str]
    task_definition_key: Optional[str]
    description: Optional[str]
    owner: Optional[str]
    delegation_state: Optional[str]
    priority: Optional[int]
    suspended: bool = False
    form_key: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create Task instance from Camunda API response."""
        
        # Convert date strings to datetime objects
        created = None
        if data.get("created"):
            created = datetime.fromisoformat(data["created"].replace('Z', '+00:00'))
        
        due = None
        if data.get("due"):
            due = datetime.fromisoformat(data["due"].replace('Z', '+00:00'))
        
        return cls(
            id=data["id"],
            name=data.get("name"),
            assignee=data.get("assignee"),
            created=created,
            due=due,
            process_instance_id=data.get("processInstanceId"),
            process_definition_id=data.get("processDefinitionId"),
            case_instance_id=data.get("caseInstanceId"),
            case_definition_id=data.get("caseDefinitionId"),
            task_definition_key=data.get("taskDefinitionKey"),
            description=data.get("description"),
            owner=data.get("owner"),
            delegation_state=data.get("delegationState"),
            priority=data.get("priority"),
            suspended=data.get("suspended", False),
            form_key=data.get("formKey")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Task instance to dictionary."""
        result = {
            "id": self.id,
            "name": self.name,
            "assignee": self.assignee,
            "processInstanceId": self.process_instance_id,
            "processDefinitionId": self.process_definition_id,
            "taskDefinitionKey": self.task_definition_key,
            "description": self.description,
            "owner": self.owner,
            "delegationState": self.delegation_state,
            "priority": self.priority,
            "suspended": self.suspended,
            "formKey": self.form_key
        }
        
        if self.created:
            result["created"] = self.created.isoformat()
        if self.due:
            result["due"] = self.due.isoformat()
            
        # Remove None values
        return {k: v for k, v in result.items() if v is not None}


@dataclass  
class ProcessInstance:
    """Represents a Camunda process instance."""
    
    id: str
    definition_id: str
    business_key: Optional[str]
    case_instance_id: Optional[str]
    ended: bool
    suspended: bool
    tenant_id: Optional[str]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProcessInstance":
        """Create ProcessInstance from Camunda API response."""
        return cls(
            id=data["id"],
            definition_id=data["definitionId"],
            business_key=data.get("businessKey"),
            case_instance_id=data.get("caseInstanceId"),
            ended=data.get("ended", False),
            suspended=data.get("suspended", False),
            tenant_id=data.get("tenantId")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ProcessInstance to dictionary."""
        result = {
            "id": self.id,
            "definitionId": self.definition_id,
            "businessKey": self.business_key,
            "caseInstanceId": self.case_instance_id,
            "ended": self.ended,
            "suspended": self.suspended,
            "tenantId": self.tenant_id
        }
        
        # Remove None values
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class Comment:
    """Represents a task comment."""
    
    id: str
    user_id: Optional[str]
    task_id: Optional[str]
    process_instance_id: Optional[str]
    time: Optional[datetime]
    message: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Comment":
        """Create Comment from Camunda API response."""
        
        # Convert time string to datetime
        time = None
        if data.get("time"):
            time = datetime.fromisoformat(data["time"].replace('Z', '+00:00'))
        
        return cls(
            id=data["id"],
            user_id=data.get("userId"),
            task_id=data.get("taskId"),
            process_instance_id=data.get("processInstanceId"),
            time=time,
            message=data["message"]
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Comment to dictionary."""
        result = {
            "id": self.id,
            "userId": self.user_id,
            "taskId": self.task_id,
            "processInstanceId": self.process_instance_id,
            "message": self.message
        }
        
        if self.time:
            result["time"] = self.time.isoformat()
            
        # Remove None values
        return {k: v for k, v in result.items() if v is not None}
