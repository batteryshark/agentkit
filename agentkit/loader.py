#!/usr/bin/env python3
"""
Simple, lightweight plugin loader.
Drop this into any project for instant plugin support.
"""

import importlib
import importlib.util
import platform
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable


class Plugins:
    """Simple plugin registry and loader."""
    
    def __init__(self, plugins_dir: str = "plugins", silent: bool = False):
        self.plugins_dir = Path(plugins_dir)
        self.silent = silent
        self.tools: Dict[str, Callable] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}
        
        # Auto-load plugins on init
        self.load_all()
    
    def _log(self, message: str) -> None:
        """Log message if not in silent mode."""
        if not self.silent:
            print(f"🔌 {message}")
    
    def _is_compatible(self, module_info: Dict[str, Any]) -> bool:
        """Check if plugin is compatible with current environment."""
        # Check platform
        platform_req = module_info.get("platform")
        if platform_req and platform_req != "any":
            current_platform = platform.system().lower()
            if isinstance(platform_req, str):
                platform_req = [platform_req]
            if isinstance(platform_req, list) and current_platform not in platform_req:
                return False
        
        # Check Python version (basic check)
        python_req = module_info.get("python_requires")
        if python_req and python_req.startswith(">="):
            try:
                min_version = tuple(map(int, python_req[2:].split('.')))
                if sys.version_info[:len(min_version)] < min_version:
                    return False
            except:
                pass  # Ignore parsing errors
        
        return True
    
    def load_plugin(self, plugin_file: Path) -> bool:
        """Load a single plugin file."""
        try:
            # Load the module
            spec = importlib.util.spec_from_file_location(plugin_file.stem, plugin_file)
            if not spec or not spec.loader:
                return False
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get module info
            module_info = getattr(module, "_module_info", {})
            if not module_info:
                self._log(f"⚠️  {plugin_file.name} missing _module_info")
                return False
            
            # Get Module Exports
            module_exports = getattr(module, "_module_exports", {})
            if not module_exports:
                self._log(f"⚠️  {plugin_file.name} missing _module_exports")
                return False
            
            # Check compatibility
            if not self._is_compatible(module_info):
                self._log(f"⚠️  {plugin_file.name} not compatible")
                return False
            
            # Register exports
            plugin_name = plugin_file.stem
            self.metadata[plugin_name] = module_info
            
            # Register tools
            for tool in module_exports.get("tools",[]):
                if callable(tool):
                    self.tools[f"{plugin_name}.{tool.__name__}"] = tool
            
            # Call initialization function if provided
            init_function = module_exports.get("init_function")
            if init_function and callable(init_function):
                try:
                    init_function()
                    self._log(f"🔧 Initialized {plugin_name}")
                except Exception as e:
                    self._log(f"⚠️  Failed to initialize {plugin_name}: {e}")
            
            name = module_info.get("name", plugin_name)
            version = module_info.get("version", "")
            self._log(f"✅ Loaded {name} {version}")
            return True
            
        except Exception as e:
            self._log(f"❌ Failed to load {plugin_file.name}: {e}")
            return False
    
    def load_package_plugin(self, plugin_dir: Path) -> bool:
        """Load a package-based plugin from a directory."""
        try:
            # Check if it has __init__.py
            init_file = plugin_dir / "__init__.py"
            if not init_file.exists():
                return False
            
            # Add the plugins directory to sys.path temporarily
            plugins_parent = str(self.plugins_dir.absolute())
            if plugins_parent not in sys.path:
                sys.path.insert(0, plugins_parent)
            
            try:
                # Import the package
                module = importlib.import_module(plugin_dir.name)
                # Force reload in case it was already imported
                importlib.reload(module)
            except ImportError as e:
                self._log(f"❌ Failed to import {plugin_dir.name}: {e}")
                return False
            finally:
                # Remove from sys.path
                if plugins_parent in sys.path:
                    sys.path.remove(plugins_parent)
            
            # Get module info
            module_info = getattr(module, "_module_info", {})
            if not module_info:
                self._log(f"⚠️  {plugin_dir.name}/ missing _module_info")
                return False
            
            # Get Module Exports
            module_exports = getattr(module, "_module_exports", {})
            if not module_exports:
                self._log(f"⚠️  {plugin_dir.name}/ missing _module_exports")
                return False
            
            # Check compatibility
            if not self._is_compatible(module_info):
                self._log(f"⚠️  {plugin_dir.name}/ not compatible")
                return False
            
            # Register exports
            plugin_name = plugin_dir.name
            self.metadata[plugin_name] = module_info
            
            # Register tools
            for tool in module_exports.get("tools", []):
                if callable(tool):
                    self.tools[f"{plugin_name}.{tool.__name__}"] = tool
            
            # Call initialization function if provided
            init_function = module_exports.get("init_function")
            if init_function and callable(init_function):
                try:
                    init_function()
                    self._log(f"🔧 Initialized {plugin_name}")
                except Exception as e:
                    self._log(f"⚠️  Failed to initialize {plugin_name}: {e}")
            
            name = module_info.get("name", plugin_name)
            version = module_info.get("version", "")
            self._log(f"✅ Loaded {name} {version} (package)")
            return True
            
        except Exception as e:
            self._log(f"❌ Failed to load {plugin_dir.name}/: {e}")
            return False

    def load_all(self) -> int:
        """Load all plugins from the plugins directory."""
        if not self.plugins_dir.exists():
            return 0
        
        loaded = 0
        
        # Load single-file plugins
        for plugin_file in self.plugins_dir.glob("*.py"):
            if not plugin_file.name.startswith("__"):
                if self.load_plugin(plugin_file):
                    loaded += 1
        
        # Load package-based plugins
        for plugin_dir in self.plugins_dir.iterdir():
            if plugin_dir.is_dir() and not plugin_dir.name.startswith("__") and plugin_dir.name != "__pycache__":
                if self.load_package_plugin(plugin_dir):
                    loaded += 1
        
        if not self.silent and loaded > 0:
            self._log(f"Loaded {loaded} plugins")
        
        return loaded
    
    def get_tool(self, name: str) -> Optional[Callable]:
        """Get a tool by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """List all available tools."""
        return list(self.tools.keys())
    
    def get_all_tools(self) -> List[Callable]:
        """Get all tools."""
        return list(self.tools.values())

    
    def list_plugins(self) -> Dict[str, Dict[str, Any]]:
        """List all loaded plugins with metadata."""
        return self.metadata.copy()


# Convenience functions for simple usage
def load_plugins(plugins_dir: str = "plugins", silent: bool = False) -> Plugins:
    """Load plugins and return the registry."""
    return Plugins(plugins_dir, silent)


if __name__ == "__main__":
    # Example usage
    plugins = load_plugins()
    
    print(f"\n📋 Summary:")
    print(f"   Plugins: {len(plugins.list_plugins())}")
    print(f"   Tools: {len(plugins.list_tools())}")
    
    if plugins.list_tools():
        print(f"\n🔧 Available tools:")
        for tool in plugins.list_tools():
            print(f"   • {tool}")
