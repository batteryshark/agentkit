# =============================================================================
# START OF MODULE METADATA
# =============================================================================
_module_info = {
    "name": "Text Processor",
    "description": "Advanced text processing utilities with multiple modules",
    "author": "AgentKit Team",
    "version": "1.0.0",
    "platform": "any",
    "python_requires": ">=3.10",
    "dependencies": ["pydantic>=2.0.0"],
    "environment_variables": {
        "TEXT_PROCESSOR_MAX_LENGTH": {
            "description": "Maximum text length to process",
            "default": "10000",
            "required": False
        }
    }
}
# =============================================================================
# END OF MODULE METADATA
# =============================================================================

# Import functions from our modules
from .core import analyze_text, summarize_text
from .utils import clean_text, count_words, extract_keywords
from .formatters import format_as_markdown, format_as_html, format_as_list

# =============================================================================
# START OF EXPORTS
# =============================================================================
_module_exports = {
    "tools": [
        analyze_text,
        summarize_text,
        clean_text,
        count_words,
        extract_keywords,
        format_as_markdown,
        format_as_html,
        format_as_list
    ]
}
# =============================================================================
# END OF EXPORTS
# ============================================================================= 