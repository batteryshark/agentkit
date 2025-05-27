"""
Utility functions for text processing.
"""

import re
from typing import Annotated
from pydantic import Field


async def clean_text(
    text: Annotated[str, Field(description="The text to clean")]
) -> str:
    """Clean text by removing extra whitespace and normalizing."""
    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    cleaned = cleaned.strip()
    
    # Normalize quotes
    cleaned = cleaned.replace('"', '"').replace('"', '"')
    cleaned = cleaned.replace(''', "'").replace(''', "'")
    
    return cleaned


async def count_words(
    text: Annotated[str, Field(description="The text to count words in")]
) -> int:
    """Count words in text, handling punctuation properly."""
    # Remove punctuation and split
    words = re.findall(r'\b\w+\b', text.lower())
    return len(words)


def _remove_markdown_syntax(text: str) -> str:
    """Helper function to remove markdown syntax."""
    # Remove headers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    
    # Remove bold/italic
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    
    # Remove links
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    
    # Remove code blocks
    text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    
    return text


async def extract_keywords(
    text: Annotated[str, Field(description="The text to extract keywords from")],
    max_keywords: Annotated[int, Field(description="Maximum number of keywords to return", ge=1, le=20)] = 10
) -> list[str]:
    """Extract simple keywords from text based on word frequency."""
    # Clean and normalize
    cleaned = await clean_text(text)
    
    # Remove common stop words (basic list)
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we',
        'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its',
        'our', 'their'
    }
    
    # Extract words and count frequency
    words = re.findall(r'\b\w+\b', cleaned.lower())
    word_freq = {}
    
    for word in words:
        if len(word) > 2 and word not in stop_words:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_words[:max_keywords]] 