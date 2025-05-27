# =============================================================================
# START OF MODULE METADATA
# =============================================================================
_module_info = {
    "name": "Simple Calculator",
    "description": "Basic arithmetic operations",
    "author": "BatteryShark",
    "version": "1.0.0",
    "platform": "any",
    "python_requires": ">=3.10",
    "dependencies": ["pydantic>=2.0.0"],
    "environment_variables": {}
}
# =============================================================================
# END OF MODULE METADATA
# =============================================================================

from typing import Annotated
from pydantic import Field


async def add_numbers(
        a: Annotated[float, Field(description="First number to add")],
        b: Annotated[float, Field(description="Second number to add")]
) -> float:
    """Add two numbers together and return the result."""
    result = a + b
    print(f"Adding {a} + {b} = {result}")
    return result


if __name__ == "__main__":
    import asyncio

    print("Testing add_numbers function directly...")
    result = asyncio.run(add_numbers(5.5, 3.2))
    print(f"Result: {result}")


# =============================================================================
# START OF EXPORTS
# =============================================================================
_module_exports = {
    "tools": [add_numbers]
}
# =============================================================================
# END OF EXPORTS
# ============================================================================= 