#!/usr/bin/env python3
"""
AgentKit CLI
Simple command-line tool for managing agent capabilities and environment.
"""

import argparse
import sys
from pathlib import Path
from .loader import load_plugins
from .env_utils import create_env_manager


def cmd_generate(args):
    """Generate .env template file."""
    plugins = load_plugins(silent=True)
    env_manager = create_env_manager(plugins)
    
    output_file = args.output or ".env.template"
    env_manager.generate_env_template(output_file)
    
    print(f"✅ Generated {output_file}")
    print(f"📦 Found {len(plugins.list_plugins())} capabilities")
    
    env_vars = env_manager.get_all_env_vars()
    required_count = sum(1 for v in env_vars.values() if v.get('required', False))
    print(f"🔧 {len(env_vars)} environment variables ({required_count} required)")


def cmd_validate(args):
    """Validate current environment configuration."""
    plugins = load_plugins(silent=True)
    env_manager = create_env_manager(plugins)
    
    missing = env_manager.validate_env_vars()
    conflicts = env_manager.check_conflicts()
    
    if not missing and not conflicts:
        print("✅ Environment configuration is valid!")
        return 0
    
    if missing:
        print("❌ Missing required environment variables:")
        for var in missing:
            print(f"   • {var}")
        print()
    
    if conflicts:
        print("⚠️  Potential naming conflicts detected:")
        for conflict in conflicts:
            print(f"   • {conflict}")
        print()
    
    return 1


def cmd_summary(args):
    """Show environment variable summary."""
    plugins = load_plugins(silent=True)
    env_manager = create_env_manager(plugins)
    
    print(env_manager.get_plugin_env_summary())


def cmd_list(args):
    """List all plugins and their tools."""
    plugins = load_plugins(silent=True)
    
    print(f"📦 Loaded Capabilities ({len(plugins.list_plugins())}):")
    print()
    
    for plugin_name, metadata in plugins.list_plugins().items():
        name = metadata.get("name", plugin_name)
        version = metadata.get("version", "unknown")
        description = metadata.get("description", "No description")
        
        print(f"🔌 {name} v{version}")
        print(f"   {description}")
        
        # Show tools
        plugin_tools = [tool for tool in plugins.list_tools() if tool.startswith(f"{plugin_name}.")]
        if plugin_tools:
            print(f"   Tools: {', '.join([t.split('.', 1)[1] for t in plugin_tools])}")
        
        # Show environment variables
        env_vars = metadata.get("environment_variables", {})
        if env_vars:
            required = [k for k, v in env_vars.items() if v.get('required', False)]
            optional = [k for k, v in env_vars.items() if not v.get('required', False)]
            
            if required:
                print(f"   Required env vars: {', '.join(required)}")
            if optional:
                print(f"   Optional env vars: {', '.join(optional)}")
        
        print()


def cmd_check(args):
    """Run all checks (validate + conflicts)."""
    plugins = load_plugins(silent=True)
    env_manager = create_env_manager(plugins)
    
    print("🔍 Running environment checks...\n")
    
    # Basic info
    print(f"📦 Loaded {len(plugins.list_plugins())} capabilities")
    print(f"🔧 Found {len(plugins.list_tools())} tools")
    
    env_vars = env_manager.get_all_env_vars()
    required_count = sum(1 for v in env_vars.values() if v.get('required', False))
    print(f"🌍 {len(env_vars)} environment variables ({required_count} required)")
    print()
    
    # Validation
    missing = env_manager.validate_env_vars()
    conflicts = env_manager.check_conflicts()
    
    if missing:
        print("❌ Missing required environment variables:")
        for var in missing:
            print(f"   • {var}")
        print()
    else:
        print("✅ All required environment variables are set")
        print()
    
    if conflicts:
        print("⚠️  Potential naming conflicts:")
        for conflict in conflicts:
            print(f"   • {conflict}")
        print()
    else:
        print("✅ No naming conflicts detected")
        print()
    
    # Recommendations
    if missing or conflicts:
        print("💡 Recommendations:")
        if missing:
            print("   • Run 'python -m agentkit generate' to create .env.template")
            print("   • Copy .env.template to .env and configure required variables")
        if conflicts:
            print("   • Consider renaming conflicting variables for clarity")
        return 1
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Manage agent capabilities and environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m agentkit generate              # Generate .env.template
  python -m agentkit generate -o .env.dev  # Generate to custom file
  python -m agentkit validate              # Check current environment
  python -m agentkit summary               # Show environment summary
  python -m agentkit list                  # List all capabilities
  python -m agentkit check                 # Run all checks
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate .env template file')
    gen_parser.add_argument('-o', '--output', help='Output file (default: .env.template)')
    gen_parser.set_defaults(func=cmd_generate)
    
    # Validate command
    val_parser = subparsers.add_parser('validate', help='Validate environment configuration')
    val_parser.set_defaults(func=cmd_validate)
    
    # Summary command
    sum_parser = subparsers.add_parser('summary', help='Show environment variable summary')
    sum_parser.set_defaults(func=cmd_summary)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all plugins and tools')
    list_parser.set_defaults(func=cmd_list)
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Run all environment checks')
    check_parser.set_defaults(func=cmd_check)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        return args.func(args) or 0
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 