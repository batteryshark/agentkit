#!/usr/bin/env python3
"""
Lightweight plugin dependency checker.
Simple preflight check for plugin dependencies and requirements file generation.
"""

import subprocess
import sys
import importlib
import re
from pathlib import Path
from typing import List, Dict, Set


def extract_dependencies_from_plugin(plugin_file: Path) -> List[str]:
    """
    Extract dependencies from plugin file by parsing the _module_info dict.
    Returns list of dependency strings.
    """
    try:
        content = plugin_file.read_text()
        
        # Look for _module_info dictionary
        module_info_match = re.search(
            r'_module_info\s*=\s*{([^}]+)}', 
            content, 
            re.DOTALL
        )
        
        if not module_info_match:
            return []
        
        module_info_content = module_info_match.group(1)
        
        # Extract dependencies list
        deps_match = re.search(
            r'"dependencies"\s*:\s*\[([^\]]+)\]',
            module_info_content
        )
        
        if not deps_match:
            return []
        
        deps_content = deps_match.group(1)
        
        # Extract individual dependency strings
        deps = re.findall(r'"([^"]+)"', deps_content)
        return deps
        
    except Exception as e:
        print(f"Error parsing {plugin_file.name}: {e}")
        return []


def check_plugin_dependencies(plugins_dir: str = "plugins") -> bool:
    """
    Simple dependency check for all plugins.
    Returns True if all dependencies are satisfied.
    """
    plugins_path = Path(plugins_dir)
    if not plugins_path.exists():
        print(f"⚠️  Plugins directory '{plugins_dir}' not found")
        return True
    
    all_deps = set()
    missing_deps = set()
    
    # Collect all dependencies
    for plugin_file in plugins_path.glob("*.py"):
        if plugin_file.name.startswith("__"):
            continue
            
        print(f"Checking dependencies for {plugin_file.stem}")
        deps = extract_dependencies_from_plugin(plugin_file)
        all_deps.update(deps)
    
    if not all_deps:
        print("ℹ️  No dependencies found in plugins")
        return True
    
    print(f"📋 Found dependencies: {', '.join(sorted(all_deps))}")
    
    # Check which dependencies are missing
    for dep in all_deps:
        # Extract package name (remove version specifiers)
        pkg_name = re.split(r'[>=<!=]', dep)[0].strip()
        try:
            importlib.import_module(pkg_name)
        except ImportError:
            missing_deps.add(dep)
    
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(sorted(missing_deps))}")
        print(f"💡 Install with: pip install {' '.join(sorted(missing_deps))}")
        return False
    
    print("✅ All plugin dependencies satisfied")
    return True


def generate_plugin_requirements(plugins_dir: str = "plugins") -> bool:
    """Generate plugin_requirements.txt file with all plugin dependencies."""
    plugins_path = Path(plugins_dir)
    if not plugins_path.exists():
        print(f"⚠️  Plugins directory '{plugins_dir}' not found")
        return True
    
    all_deps = set()
    
    # Collect all dependencies
    for plugin_file in plugins_path.glob("*.py"):
        if plugin_file.name.startswith("__"):
            continue
            
        deps = extract_dependencies_from_plugin(plugin_file)
        all_deps.update(deps)
    
    if not all_deps:
        print("ℹ️  No plugin dependencies found")
        # Remove existing requirements file if no dependencies
        req_file = Path("plugin_requirements.txt")
        if req_file.exists():
            req_file.unlink()
            print("🗑️  Removed empty plugin_requirements.txt")
        return True
    
    # Write requirements file
    req_file = Path("plugin_requirements.txt")
    try:
        with req_file.open("w") as f:
            f.write("# Plugin dependencies\n")
            f.write("# Install with: pip install -r plugin_requirements.txt\n\n")
            for dep in sorted(all_deps):
                f.write(f"{dep}\n")
        
        print(f"📝 Generated plugin_requirements.txt with {len(all_deps)} dependencies")
        print(f"💡 Install with: pip install -r plugin_requirements.txt")
        return True
    except Exception as e:
        print(f"❌ Failed to write plugin_requirements.txt: {e}")
        return False


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Check plugin dependencies and generate requirements file")
    parser.add_argument("--generate", action="store_true", help="Generate plugin_requirements.txt file")
    parser.add_argument("--plugins-dir", default="plugins", help="Plugins directory")
    
    args = parser.parse_args()
    
    if args.generate:
        success = generate_plugin_requirements(args.plugins_dir)
    else:
        success = check_plugin_dependencies(args.plugins_dir)
    
    sys.exit(0 if success else 1) 