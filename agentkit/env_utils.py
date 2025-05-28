#!/usr/bin/env python3
"""
Plugin Environment Variable Utilities
Helps manage environment variables across plugins in a clean, documented way.
"""

import os
from typing import Dict, Any, List, Optional
from pathlib import Path


class PluginEnvManager:
    """Manages environment variables for plugins."""
    
    def __init__(self, plugins_registry):
        self.plugins = plugins_registry
    
    def get_all_env_vars(self) -> Dict[str, Dict[str, Any]]:
        """Get all environment variables from all loaded plugins."""
        all_env_vars = {}
        
        for plugin_name, metadata in self.plugins.list_plugins().items():
            env_vars = metadata.get("environment_variables", {})
            for var_name, var_info in env_vars.items():
                all_env_vars[var_name] = {
                    **var_info,
                    "plugin": plugin_name,
                    "plugin_display_name": metadata.get("name", plugin_name)
                }
        
        return all_env_vars
    
    def generate_env_template(self, output_file: str = ".env.template") -> str:
        """Generate a .env template file with all plugin environment variables."""
        env_vars = self.get_all_env_vars()
        
        template_lines = [
            "# =============================================================================",
            "# PLUGIN ENVIRONMENT VARIABLES TEMPLATE",
            "# =============================================================================",
            "# This file was auto-generated from plugin metadata.",
            "# Copy to .env and customize as needed.",
            "#",
            ""
        ]
        
        # Group by plugin
        plugins_processed = set()
        for var_name, var_info in env_vars.items():
            plugin_name = var_info["plugin"]
            plugin_display = var_info["plugin_display_name"]
            
            if plugin_name not in plugins_processed:
                template_lines.extend([
                    f"# -----------------------------------------------------------------------------",
                    f"# {plugin_display} ({plugin_name})",
                    f"# -----------------------------------------------------------------------------"
                ])
                plugins_processed.add(plugin_name)
            
            # Add variable documentation
            template_lines.append(f"# {var_info.get('description', 'No description')}")
            if var_info.get('required', False):
                template_lines.append(f"# REQUIRED")
            else:
                template_lines.append(f"# Optional (default: {var_info.get('default', 'None')})")
            
            # Add the variable line
            if var_info.get('required', False):
                template_lines.append(f"{var_name}=")
            else:
                default_val = var_info.get('default', '')
                template_lines.append(f"# {var_name}={default_val}")
            
            template_lines.append("")
        
        template_content = "\n".join(template_lines)
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write(template_content)
        
        return template_content
    
    def validate_env_vars(self) -> List[str]:
        """Validate that all required environment variables are set."""
        missing_vars = []
        env_vars = self.get_all_env_vars()
        
        for var_name, var_info in env_vars.items():
            if var_info.get('required', False) and not os.getenv(var_name):
                plugin_display = var_info["plugin_display_name"]
                missing_vars.append(f"{var_name} (required by {plugin_display})")
        
        return missing_vars
    
    def get_plugin_env_summary(self) -> str:
        """Get a summary of environment variables by plugin."""
        env_vars = self.get_all_env_vars()
        
        summary_lines = ["Plugin Environment Variables Summary:", ""]
        
        # Group by plugin
        plugin_vars = {}
        for var_name, var_info in env_vars.items():
            plugin = var_info["plugin_display_name"]
            if plugin not in plugin_vars:
                plugin_vars[plugin] = []
            plugin_vars[plugin].append((var_name, var_info))
        
        for plugin, vars_list in plugin_vars.items():
            summary_lines.append(f"📦 {plugin}:")
            for var_name, var_info in vars_list:
                status = "REQUIRED" if var_info.get('required', False) else "optional"
                current_val = os.getenv(var_name, var_info.get('default', 'unset'))
                summary_lines.append(f"   • {var_name} ({status})")
            summary_lines.append("")
        
        return "\n".join(summary_lines)
    
    def check_conflicts(self) -> List[str]:
        """Check for potential environment variable naming conflicts."""
        conflicts = []
        env_vars = self.get_all_env_vars()
        
        # Look for variables that might conflict (similar names, common patterns)
        var_names = list(env_vars.keys())
        
        # Check for exact duplicates (shouldn't happen with good naming)
        seen_bases = {}
        for var_name in var_names:
            # Extract base name (everything after last underscore)
            parts = var_name.split('_')
            if len(parts) > 1:
                base = parts[-1]
                if base in seen_bases:
                    conflicts.append(f"Potential conflict: {var_name} and {seen_bases[base]} both end with '{base}'")
                else:
                    seen_bases[base] = var_name
        
        return conflicts


def create_env_manager(plugins_registry) -> PluginEnvManager:
    """Create an environment manager for the given plugins registry."""
    return PluginEnvManager(plugins_registry)


if __name__ == "__main__":
    # Example usage
    from .loader import load_plugins
    
    plugins = load_plugins()
    env_manager = create_env_manager(plugins)
    
    print("🔧 Generating .env template...")
    env_manager.generate_env_template()
    print("✅ Created .env.template")
    
    print("\n" + env_manager.get_plugin_env_summary())
    
    missing = env_manager.validate_env_vars()
    if missing:
        print(f"\n⚠️  Missing required environment variables:")
        for var in missing:
            print(f"   • {var}")
    else:
        print(f"\n✅ All required environment variables are set")
    
    conflicts = env_manager.check_conflicts()
    if conflicts:
        print(f"\n⚠️  Potential naming conflicts:")
        for conflict in conflicts:
            print(f"   • {conflict}") 
