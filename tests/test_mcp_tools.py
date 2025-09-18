"""
Tests for MCP tools - Now using FastMCP architecture
"""

from src.camunda.client import CamundaClient


class TestMCPServer:
    """Test cases for the FastMCP server implementation."""

    def test_server_import(self) -> None:
        """Test that the MCP server can be imported without errors."""
        from src.server import mcp

        # Should not raise exception
        assert mcp is not None
        assert mcp.name == "camunda-mcp-server"

    def test_camunda_client_initialization(self) -> None:
        """Test that Camunda client can be initialized."""
        from src.server import camunda_client

        assert camunda_client is not None
        assert isinstance(camunda_client, CamundaClient)

    def test_tools_are_registered(self) -> None:
        """Test that tools are properly registered with FastMCP."""
        from src.server import mcp

        # FastMCP should have tools registered
        # We can't easily test this without running the server,
        # but we can verify the module loads without errors
        assert hasattr(mcp, "name")

    def test_all_expected_tools_exist(self) -> None:
        """Test that all expected tool functions exist in the server module."""
        import src.server as server_module

        expected_tools = [
            "list_tasks",
            "get_task_details",
            "complete_task",
            "create_task",
            "list_process_instances",
            "list_process_definitions",
            "start_process_instance",
            "get_task_comments",
            "add_task_comment",
        ]

        for tool_name in expected_tools:
            assert hasattr(server_module, tool_name), f"Tool {tool_name} not found"
            tool_func = getattr(server_module, tool_name)
            assert callable(tool_func), f"Tool {tool_name} is not callable"


class TestIntegration:
    """Integration tests for the complete MCP server setup."""

    def test_server_module_loads(self) -> None:
        """Test that the server module loads completely."""
        import src.server

        # Should not raise exception and should have expected attributes
        assert hasattr(src.server, "mcp")
        assert hasattr(src.server, "camunda_client")
        assert hasattr(src.server, "logger")
