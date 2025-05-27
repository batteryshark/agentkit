"""
Text formatting functions.
"""

import re
from typing import Annotated
from pydantic import Field


async def format_as_markdown(
    text: Annotated[str, Field(description="The text to format as markdown")],
    title: Annotated[str, Field(description="Title for the markdown document")] = "Document"
) -> str:
    """Format text as a markdown document with basic structure."""
    lines = text.split('\n')
    formatted_lines = [f"# {title}", ""]
    
    current_paragraph = []
    
    for line in lines:
        line = line.strip()
        
        if not line:  # Empty line
            if current_paragraph:
                formatted_lines.append(' '.join(current_paragraph))
                formatted_lines.append("")
                current_paragraph = []
        else:
            current_paragraph.append(line)
    
    # Add final paragraph if exists
    if current_paragraph:
        formatted_lines.append(' '.join(current_paragraph))
    
    return '\n'.join(formatted_lines)


async def format_as_html(
    text: Annotated[str, Field(description="The text to format as HTML")],
    title: Annotated[str, Field(description="Title for the HTML document")] = "Document"
) -> str:
    """Format text as a simple HTML document."""
    # Escape HTML characters
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    # Split into paragraphs
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    html_paragraphs = []
    for paragraph in paragraphs:
        # Replace line breaks within paragraphs with spaces
        paragraph = re.sub(r'\n+', ' ', paragraph)
        html_paragraphs.append(f"    <p>{paragraph}</p>")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        p {{
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
{chr(10).join(html_paragraphs)}
</body>
</html>"""
    
    return html_content


async def format_as_list(
    text: Annotated[str, Field(description="The text to format as a list")],
    list_type: Annotated[str, Field(description="Type of list: 'bullet' or 'numbered'")] = "bullet"
) -> str:
    """Format text as a bulleted or numbered list."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    if list_type == "numbered":
        formatted_lines = [f"{i+1}. {line}" for i, line in enumerate(lines)]
    else:  # bullet
        formatted_lines = [f"• {line}" for line in lines]
    
    return '\n'.join(formatted_lines) 