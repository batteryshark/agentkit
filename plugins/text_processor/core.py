"""
Core text processing functions.
"""

import os
import re
from typing import Annotated, Dict, Any
from pydantic import Field

from .utils import clean_text, count_words


async def analyze_text(
    text: Annotated[str, Field(description="The text to analyze")]
) -> Dict[str, Any]:
    """Analyze text and return comprehensive statistics."""
    max_length = int(os.getenv("TEXT_PROCESSOR_MAX_LENGTH", "10000"))
    
    if len(text) > max_length:
        raise ValueError(f"Text too long. Maximum length is {max_length} characters.")
    
    # Clean the text first
    cleaned = await clean_text(text)
    
    # Basic statistics
    char_count = len(text)
    char_count_no_spaces = len(text.replace(" ", ""))
    word_count = await count_words(text)
    line_count = len(text.split('\n'))
    paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
    
    # Sentence count (basic)
    sentence_count = len(re.findall(r'[.!?]+', text))
    
    # Average word length
    words = text.split()
    avg_word_length = sum(len(word.strip('.,!?;:')) for word in words) / len(words) if words else 0
    
    return {
        "character_count": char_count,
        "character_count_no_spaces": char_count_no_spaces,
        "word_count": word_count,
        "line_count": line_count,
        "paragraph_count": paragraph_count,
        "sentence_count": sentence_count,
        "average_word_length": round(avg_word_length, 2),
        "reading_time_minutes": round(word_count / 200, 1)  # Assuming 200 WPM
    }


async def summarize_text(
    text: Annotated[str, Field(description="The text to summarize")],
    max_sentences: Annotated[int, Field(description="Maximum number of sentences in summary", ge=1, le=10)] = 3
) -> str:
    """Create a simple extractive summary of the text."""
    max_length = int(os.getenv("TEXT_PROCESSOR_MAX_LENGTH", "10000"))
    
    if len(text) > max_length:
        raise ValueError(f"Text too long. Maximum length is {max_length} characters.")
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) <= max_sentences:
        return text
    
    # Simple scoring: prefer sentences with more words (basic heuristic)
    scored_sentences = []
    for i, sentence in enumerate(sentences):
        word_count = len(sentence.split())
        # Prefer sentences in the beginning and middle
        position_score = 1.0 if i < len(sentences) * 0.3 else 0.5
        score = word_count * position_score
        scored_sentences.append((score, sentence))
    
    # Sort by score and take top sentences
    scored_sentences.sort(reverse=True)
    top_sentences = [sentence for _, sentence in scored_sentences[:max_sentences]]
    
    # Maintain original order
    summary_sentences = []
    for sentence in sentences:
        if sentence in top_sentences:
            summary_sentences.append(sentence)
            if len(summary_sentences) >= max_sentences:
                break
    
    return '. '.join(summary_sentences) + '.' 