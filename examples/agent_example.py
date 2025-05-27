from pydantic_ai import Agent
from agentkit import load_plugins
from dotenv import load_dotenv

load_dotenv()
tool_plugins = load_plugins()

test_agent = Agent(  
    'google-gla:gemini-2.0-flash',
    deps_type=int,
    output_type=bool,
    system_prompt="You are a helpful assistant that can answer questions and help with tasks.",
    tools=[tool_plugins.get_tool(tool) for tool in tool_plugins.list_tools()]
)

# Run the agent
import asyncio
asyncio.run(test_agent.run("What is 4 + 5, notify me when finished."))