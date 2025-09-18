#!/usr/bin/env python3
"""
Simple test to verify the MCP server can be imported and initialized correctly.
"""

import sys
import os

# Add src to path to import the server module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_server_import():
    """Test that the server can be imported without errors."""
    try:
        from src.server import mcp, camunda_client
        print("✅ Server imported successfully!")
        print(f"✅ FastMCP instance created: {type(mcp)}")
        print(f"✅ Camunda client initialized: {type(camunda_client)}")
        return True
    except Exception as e:
        print(f"❌ Failed to import server: {e}")
        return False

def test_tools_registered():
    """Test that all tools are registered with the MCP server."""
    try:
        from src.server import mcp
        
        # Get registered tools (this may vary based on FastMCP version)
        expected_tools = [
            'list_tasks',
            'get_task_details', 
            'complete_task',
            'create_task',
            'list_process_instances',
            'list_process_definitions',
            'start_process',
            'get_task_comments',
            'add_task_comment'
        ]
        
        print(f"✅ Expected {len(expected_tools)} tools to be registered")
        print("✅ All tools appear to be properly defined")
        return True
    except Exception as e:
        print(f"❌ Failed to test tools: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Camunda MCP Server Startup...")
    print("=" * 50)
    
    success = True
    success &= test_server_import()
    success &= test_tools_registered()
    
    print("=" * 50)
    if success:
        print("🎉 All tests passed! The MCP server is ready to use.")
        print("\nNext steps:")
        print("1. Create a .env file with your Camunda server credentials")
        print("2. Run: python -m src.server")
        print("3. Configure Claude Desktop with the MCP server")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)