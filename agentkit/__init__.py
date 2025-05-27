"""
AgentKit
A lightweight, flexible toolkit for extending AI agents and MCP servers with modular capabilities.
"""

from .loader import Plugins, load_plugins
from .env_utils import PluginEnvManager, create_env_manager
from .depcheck import (
    check_plugin_dependencies,
    generate_plugin_requirements,
    extract_dependencies_from_plugin
)

__version__ = "1.0.0"
__author__ = "BatteryShark"

# Convenience exports
__all__ = [
    "Plugins",
    "load_plugins", 
    "PluginEnvManager",
    "create_env_manager",
    "check_plugin_dependencies",
    "generate_plugin_requirements",
    "extract_dependencies_from_plugin"
] 