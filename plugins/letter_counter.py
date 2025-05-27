# =============================================================================
# START OF MODULE METADATA
# =============================================================================
_module_info = {
    "name": "Letter Counter",
    "description": "Count occurrences of specific letters in words",
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


async def count_letter_in_word(
        word: Annotated[str, Field(description="The word to search in")],
        letter: Annotated[str, Field(description="The letter to count (single character)")]
) -> int:
    """Count how many times a specific letter appears in a word."""
    # Convert both to lowercase for case-insensitive counting
    word_lower = word.lower()
    letter_lower = letter.lower()
    
    # Validate that letter is a single character
    if len(letter) != 1:
        print(f"Error: '{letter}' is not a single character")
        return 0
    
    count = word_lower.count(letter_lower)
    print(f"The letter '{letter}' appears {count} times in '{word}'")
    return count


if __name__ == "__main__":
    import asyncio

    print("Testing letter counting function...")
    
    # The famous strawberry example
    result1 = asyncio.run(count_letter_in_word("strawberry", "r"))
    print(f"Result: {result1}")
    
    # A few more examples
    result2 = asyncio.run(count_letter_in_word("hello", "l"))
    print(f"Result: {result2}")
    
    result3 = asyncio.run(count_letter_in_word("Mississippi", "s"))
    print(f"Result: {result3}")


# =============================================================================
# START OF EXPORTS
# =============================================================================
_module_exports = {
    "tools": [count_letter_in_word]
}
# =============================================================================
# END OF EXPORTS
# ============================================================================= 