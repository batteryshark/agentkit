# =============================================================================
# START OF MODULE METADATA
# =============================================================================
_module_info = {
    "name": "MacOS Notifier",
    "description": "MacOS user notification functionality",
    "author": "BatteryShark",
    "version": "1.0.0",
    "platform": "darwin",
    "python_requires": ">=3.10",
    "dependencies": ["pydantic>=2.0.0", "pync>=2.0.0"],
    "environment_variables": {
        "MACOS_NOTIFIER_DEFAULT_SOUND": {
            "description": "Default notification sound",
            "default": "Ping",
            "required": False
        },
        "MACOS_NOTIFIER_ENABLED": {
            "description": "Enable/disable notifications",
            "default": "true",
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

import pync


async def send_notification(
        message: Annotated[str, Field(description="The notification message")],
        title: Annotated[str, Field(description="Optional notification title")] = None
) -> bool:
    """Send a MacOS notification popup to the user."""
    # Check if notifications are enabled
    if os.getenv("MACOS_NOTIFIER_ENABLED", "true").lower() == "false":
        print("MacOS notifications are disabled")
        return False
    
    try:
        sound = os.getenv("MACOS_NOTIFIER_DEFAULT_SOUND", "Ping")
        pync.notify(message, title=title, sound=sound)
        return True
    except Exception as e:
        print(f"Failed to send notification: {e}")
        return False

if __name__ == "__main__":
    import asyncio

    print("Testing notification function directly...")
    asyncio.run(send_notification("Hello, World!", "Test Title"))
    

# =============================================================================
# START OF EXPORTS
# =============================================================================
_module_exports = {
    "tools": [send_notification]
}
# =============================================================================
# END OF EXPORTS
# =============================================================================
