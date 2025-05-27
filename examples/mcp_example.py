import os
import asyncio
from fastmcp import FastMCP
from agentkit import load_plugins, create_env_manager

from dotenv import load_dotenv
load_dotenv()

# =============================================================================
# Simple, Terrible, Authentication POC for MCP Requests
# =============================================================================
from fastmcp.server.dependencies import get_http_request
from starlette.requests import Request
from functools import wraps

TEST_API_KEY = "sk-proj-1234567890"
def authentication_required_wrapper(func):
    """Decorator to authenticate tool calls via API key header."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            request: Request = get_http_request()                       
            api_key = request.headers.get("Authorization")
            # LOL
            if api_key != f"Bearer {TEST_API_KEY}":
                return {"error": "Authentication failed: Invalid or missing API key"}
            return await func(*args, **kwargs)
        except Exception as e:
            return {"error": f"Authentication error: {str(e)}"}
    return wrapper
# =============================================================================

# -- MCP CONFIG --
MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
MCP_PORT = int(os.getenv("MCP_PORT", 5055))
MCP_TRANSPORT = os.getenv("MCP_TRANSPORT", "streamable-http")
MCP_NAME = os.getenv("MCP_NAME", "HTTP Request Demo")

mcp = FastMCP(name=MCP_NAME)

# Load plugins and check environment configuration
tool_plugins = load_plugins()
env_manager = create_env_manager(tool_plugins)

# Validate environment variables
missing_vars = env_manager.validate_env_vars()
if missing_vars:
    print("⚠️  Missing required environment variables:")
    for var in missing_vars:
        print(f"   • {var}")
    print("\n💡 Run 'python -m agentkit generate' to generate .env.template")
    print("   Then copy to .env and configure required variables")

# Show environment summary
print("\n" + env_manager.get_plugin_env_summary())

# Add tools to MCP server
for tool in tool_plugins.list_tools():
    print(f"Adding tool to MCP Server: {tool}")
    mcp.add_tool(tool_plugins.get_tool(tool))
    # Alternatively, you can use the authentication_required_wrapper to wrap the tools
    # This will require the user to authenticate before using the tools
    # mcp.add_tool(authentication_required_wrapper(tool_plugins.get_tool(tool)))    



if __name__ == "__main__":
    asyncio.run(mcp.run(transport=MCP_TRANSPORT, host=MCP_HOST, port=MCP_PORT))