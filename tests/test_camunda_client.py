"""
Tests for Camunda REST API client
"""

from unittest.mock import Mock, patch
from datetime import datetime
from typing import Iterator
from contextlib import contextmanager
from src.camunda.client import CamundaClient, CamundaConfig
from src.camunda.models import Task, ProcessInstance, Comment


@contextmanager
def camunda_test_environment(
    url: str = "http://localhost:8080/engine-rest",
    username: str = "demo", 
    password: str = "demo",
    auth_type: str = "basic"
) -> Iterator[CamundaConfig]:
    """
    Context manager for test environment configuration.
    
    Uses the same environment variable keys as client.py:
    - CAMUNDA_URL
    - CAMUNDA_USERNAME  
    - CAMUNDA_PASSWORD
    - CAMUNDA_AUTH_TYPE
    
    Usage:
        with test_environment() as config:
            client = CamundaClient(config)
            
        # Or with custom values:
        with test_environment(url="http://test-server:8080") as config:
            client = CamundaClient(config)
    """
    with patch.dict('os.environ', {
        'CAMUNDA_URL': url,
        'CAMUNDA_USERNAME': username,
        'CAMUNDA_PASSWORD': password,
        'CAMUNDA_AUTH_TYPE': auth_type
    }):
        yield CamundaConfig.from_environment()


class TestCamundaClient:
    """Test cases for CamundaClient."""
    
    def test_config_from_environment(self) -> None:
        """Test configuration creation from environment variables."""
        with camunda_test_environment(
            url='http://test-camunda:8080/engine-rest',
            username='testuser',
            password='testpass',
            auth_type='basic'
        ) as config:
            assert config.url == 'http://test-camunda:8080/engine-rest'
            assert config.username == 'testuser'
            assert config.password == 'testpass'
            assert config.auth_type == 'basic'
    
    def test_config_with_oauth(self) -> None:
        """Test configuration with OAuth authentication."""
        with camunda_test_environment(
            url='https://production-camunda.company.com/engine-rest',
            username='oauth-client',
            password='oauth-secret',
            auth_type='oauth'
        ) as config:
            assert config.url == 'https://production-camunda.company.com/engine-rest'
            assert config.username == 'oauth-client'
            assert config.password == 'oauth-secret'
            assert config.auth_type == 'oauth'
    
    def test_client_initialization(self) -> None:
        """Test client initialization with configuration."""
        with camunda_test_environment() as config:
            client = CamundaClient(config)
            
            assert client.config == config
            assert client.session is not None
            assert config.url == 'http://localhost:8080/engine-rest'
            assert config.username == 'demo'
            assert config.password == 'demo'
            assert config.auth_type == 'basic'
    
    @patch('src.camunda.client.requests.Session.request')
    def test_get_tasks_success(self, mock_request: Mock) -> None:
        """Test successful task retrieval."""
        # Mock response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [{
            'id': 'task-123',
            'name': 'Test Task',
            'assignee': 'testuser',
            'created': '2024-01-01T10:00:00.000Z',
            'processInstanceId': 'proc-456'
        }]
        mock_request.return_value = mock_response
        
        with camunda_test_environment() as config:
            client = CamundaClient(config)
            tasks = client.get_tasks()
        
        assert len(tasks) == 1
        assert tasks[0].id == 'task-123'
        assert tasks[0].name == 'Test Task'
        assert tasks[0].assignee == 'testuser'
    
    @patch('src.camunda.client.requests.Session.request')
    def test_complete_task_success(self, mock_request: Mock) -> None:
        """Test successful task completion."""
        # Mock response for task completion (empty response)
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.status_code = 204
        mock_response.content = b''
        mock_request.return_value = mock_response
        
        with camunda_test_environment() as config:
            client = CamundaClient(config)
            
            # Should not raise exception
            client.complete_task('task-123', {'result': 'approved'})
        
        # Verify the request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        
        assert args[0] == 'POST'
        assert 'task/task-123/complete' in args[1]
        assert 'json' in kwargs
    
    @patch('src.camunda.client.requests.Session.request')
    def test_health_check_success(self, mock_request: Mock) -> None:
        """Test successful health check."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [{'name': 'default'}]
        mock_request.return_value = mock_response
        
        with camunda_test_environment() as config:
            client = CamundaClient(config)
            result = client.health_check()
        
        assert result is True
    
    @patch('src.camunda.client.requests.Session.request')
    def test_health_check_failure(self, mock_request: Mock) -> None:
        """Test health check failure."""
        mock_request.side_effect = Exception("Connection failed")
        
        with camunda_test_environment() as config:
            client = CamundaClient(config)
            result = client.health_check()
        
        assert result is False

    def test_integration_with_env_file(self) -> None:
        """
        Integration test that uses actual .env file configuration.
        
        To run this test with your actual Camunda server:
        1. Create a .env file with your Camunda credentials
        2. Uncomment the test code below
        3. Run: pytest tests/test_camunda_client.py::TestCamundaClient::\
               test_integration_with_env_file
        
        Note: This test is commented out by default to avoid requiring 
        a running Camunda server during normal test runs.
        """
        # Uncomment to test with actual .env configuration:
        
        # from dotenv import load_dotenv
        # load_dotenv()  # Load .env file
        # 
        # config = CamundaConfig.from_environment()
        # client = CamundaClient(config)
        # 
        # # Test connection
        # assert client.health_check() is True
        # 
        # # Test getting tasks (might be empty, that's OK)
        # tasks = client.get_tasks()
        # assert isinstance(tasks, list)
        
        pass  # Remove this when uncommenting above


class TestCamundaModels:
    """Test cases for Camunda data models."""
    
    def test_task_from_dict(self) -> None:
        """Test Task creation from dictionary."""
        task_data = {
            'id': 'task-123',
            'name': 'Test Task',
            'assignee': 'testuser',
            'created': '2024-01-01T10:00:00.000Z',
            'processInstanceId': 'proc-456',
            'priority': 50,
            'suspended': False
        }
        
        task = Task.from_dict(task_data)
        
        assert task.id == 'task-123'
        assert task.name == 'Test Task'
        assert task.assignee == 'testuser'
        assert task.process_instance_id == 'proc-456'
        assert task.priority == 50
        assert task.suspended is False
        assert isinstance(task.created, datetime)
    
    def test_task_to_dict(self) -> None:
        """Test Task conversion to dictionary."""
        task = Task(
            id='task-123',
            name='Test Task',
            assignee='testuser',
            created=datetime(2024, 1, 1, 10, 0),
            due=None,
            process_instance_id='proc-456',
            process_definition_id=None,
            case_instance_id=None,
            case_definition_id=None,
            task_definition_key='userTask',
            description='Test description',
            owner=None,
            delegation_state=None,
            priority=50,
            suspended=False
        )
        
        result = task.to_dict()
        
        assert result['id'] == 'task-123'
        assert result['name'] == 'Test Task'
        assert result['assignee'] == 'testuser'
        assert result['processInstanceId'] == 'proc-456'
        assert result['priority'] == 50
        # None values should be filtered out
        assert 'due' not in result
        assert 'owner' not in result
    
    def test_process_instance_from_dict(self) -> None:
        """Test ProcessInstance creation from dictionary."""
        pi_data = {
            'id': 'proc-456',
            'definitionId': 'def-789',
            'businessKey': 'BK-001',
            'ended': False,
            'suspended': False
        }
        
        pi = ProcessInstance.from_dict(pi_data)
        
        assert pi.id == 'proc-456'
        assert pi.definition_id == 'def-789'
        assert pi.business_key == 'BK-001'
        assert pi.ended is False
        assert pi.suspended is False
    
    def test_comment_from_dict(self) -> None:
        """Test Comment creation from dictionary."""
        comment_data = {
            'id': 'comment-123',
            'userId': 'testuser',
            'taskId': 'task-456',
            'time': '2024-01-01T10:30:00.000Z',
            'message': 'This is a test comment'
        }
        
        comment = Comment.from_dict(comment_data)
        
        assert comment.id == 'comment-123'
        assert comment.user_id == 'testuser'
        assert comment.task_id == 'task-456'
        assert comment.message == 'This is a test comment'
        assert isinstance(comment.time, datetime)
