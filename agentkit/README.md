# AgentKit

A lightweight, flexible toolkit for extending AI agents and MCP servers with modular capabilities.

## Features

- 🔌 **Drop-in Capabilities**: Add new tools by simply dropping Python files in a folder
- 🤖 **AI Agent Ready**: Perfect for Pydantic AI, LangChain, and other agent frameworks
- 🌐 **MCP Server Support**: Built-in integration with Model Context Protocol servers
- 🌍 **Smart Environment Management**: Automatic `.env` template generation and validation
- 📦 **Dependency Handling**: Automatic dependency detection and requirements management
- 🛠️ **CLI Tools**: Command-line interface for managing capabilities
- 🔧 **Platform Aware**: Built-in platform and Python version compatibility checking
- 📋 **Rich Metadata**: Comprehensive capability descriptions, versions, and requirements

## Quick Start

### Installation

```bash
# Install the package
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Basic Usage

```python
from agentkit import load_plugins

# Load all capabilities from the plugins/ directory
capabilities = load_plugins()

# List available tools
print(capabilities.list_tools())

# Get a specific tool for your agent
notification_tool = capabilities.get_tool("macos_notifier.send_notification")

# Use with your AI agent
result = await notification_tool("Hello from AgentKit!", "Welcome")
```

### CLI Usage

```bash
# List all available capabilities
python -m agentkit list

# Generate environment template
python -m agentkit generate

# Validate environment configuration
python -m agentkit validate

# Show environment summary
python -m agentkit summary

# Run all checks
python -m agentkit check
```

## Plugin Development

AgentKit supports two types of plugins:

1. **Single-file plugins** - Simple plugins in a single `.py` file
2. **Package plugins** - Complex plugins organized as Python packages with multiple modules

### Single-File Plugin Structure

Create a Python file in the `plugins/` directory with this structure:

```python
# =============================================================================
# START OF MODULE METADATA
# =============================================================================
_module_info = {
    "name": "My Plugin",
    "description": "What this plugin does",
    "author": "Your Name",
    "version": "1.0.0",
    "platform": "darwin",  # Optional: "darwin", "linux", "windows"
    "python_requires": ">=3.10",  # Optional
    "dependencies": ["requests>=2.0.0"],  # Optional
    "environment_variables": {  # Optional
        "MY_PLUGIN_API_KEY": {
            "description": "API key for my service",
            "required": True
        },
        "MY_PLUGIN_TIMEOUT": {
            "description": "Request timeout in seconds",
            "default": "30",
            "required": False
        }
    }
}
# =============================================================================
# END OF MODULE METADATA
# =============================================================================

import os
from typing import Annotated
from pydantic import Field

async def my_function(
    message: Annotated[str, Field(description="The message to process")]
) -> str:
    """Process a message and return a result."""
    api_key = os.getenv("MY_PLUGIN_API_KEY")
    timeout = int(os.getenv("MY_PLUGIN_TIMEOUT", "30"))
    
    # Your plugin logic here
    return f"Processed: {message}"

# =============================================================================
# START OF EXPORTS
# =============================================================================
_module_exports = {
    "tools": [my_function]
}
# =============================================================================
# END OF EXPORTS
# =============================================================================
```

### Package Plugin Structure

For complex plugins with multiple modules, create a directory in `plugins/` with an `__init__.py` file:

```
plugins/
├── my_complex_plugin/
│   ├── __init__.py          # Contains _module_info and _module_exports
│   ├── core.py              # Main functionality
│   ├── utils.py             # Helper functions
│   ├── models.py            # Data models
│   └── resources/
│       └── config.json
└── simple_plugin.py         # Single-file plugins still work
```

The `__init__.py` file should follow the same structure as single-file plugins:

```python
# =============================================================================
# START OF MODULE METADATA
# =============================================================================
_module_info = {
    "name": "My Complex Plugin",
    "description": "A plugin with multiple modules",
    "author": "Your Name",
    "version": "1.0.0",
    "platform": "any",
    "python_requires": ">=3.10",
    "dependencies": ["requests>=2.0.0"],
    "environment_variables": {
        "MY_PLUGIN_API_KEY": {
            "description": "API key for my service",
            "required": True
        }
    }
}
# =============================================================================
# END OF MODULE METADATA
# =============================================================================

# Import functions from your modules
from .core import main_function
from .utils import helper_function

# =============================================================================
# START OF EXPORTS
# =============================================================================
_module_exports = {
    "tools": [main_function, helper_function]
}
# =============================================================================
# END OF EXPORTS
# =============================================================================
```

### Benefits of Package Plugins

Package plugins are ideal for:
- **Complex functionality** that requires multiple modules
- **Shared utilities** between plugin functions
- **Resource management** (templates, configs, data files)
- **Better organization** and maintainability
- **Code reuse** and modular design

### Environment Variables

The plugin system automatically:
- Detects environment variables from plugin metadata
- Generates `.env.template` files with documentation
- Validates required variables are set
- Checks for naming conflicts

### Dependencies

The plugin system can:
- Extract dependencies from plugin metadata
- Check if dependencies are installed
- Generate `plugin_requirements.txt` files

```bash
# Check dependencies
python -m plugin_system.depcheck

# Generate requirements file
python -m plugin_system.depcheck --generate
```

## API Reference

### Core Classes

#### `Plugins`

Main plugin registry and loader.

```python
plugins = Plugins(plugins_dir="plugins", silent=False)
plugins.load_all()  # Load all plugins
plugins.get_tool("plugin.function")  # Get specific tool
plugins.list_tools()  # List all tools
plugins.list_plugins()  # List all plugins with metadata
```

#### `PluginEnvManager`

Environment variable management.

```python
from plugin_system import create_env_manager

env_manager = create_env_manager(plugins)
env_manager.generate_env_template()  # Generate .env.template
env_manager.validate_env_vars()  # Check required vars
env_manager.get_plugin_env_summary()  # Show summary
```

### Convenience Functions

```python
from plugin_system import (
    load_plugins,
    create_env_manager,
    check_plugin_dependencies,
    generate_plugin_requirements
)

# Load plugins
plugins = load_plugins()

# Environment management
env_manager = create_env_manager(plugins)

# Dependency checking
check_plugin_dependencies()
generate_plugin_requirements()
```

## Examples

See the parent directory for complete examples:
- `agent_example.py` - Using with AI agents
- `mcp_example.py` - Using with MCP servers

## License

MIT License - see LICENSE file for details. 