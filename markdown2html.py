#!/usr/bin/python3
"""
Markdown to HTML converter script that parses headings.
"""

import sys
import os

def convert_markdown_to_html(markdown_file: str, output_file: str) -> None:
    """Converts Markdown headings to HTML and writes to an output file."""
    with open(markdown_file, 'r') as md_file, open(output_file, 'w') as html_file:
        for line in md_file:
            line = line.rstrip()  # Remove trailing whitespace
            if line.startswith('#'):  # Check if the line is a heading
                heading_level = line.count('#')  # Count the number of '#' characters
                heading_text = line[heading_level:].strip()  # Extract heading text
                # Create the corresponding HTML tag
                html_file.write(f"<h{heading_level}>{heading_text}</h{heading_level}>\n")

if __name__ == '__main__':
    # Check if the number of arguments is less than 2
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    # Assign arguments to variables
    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    # Convert the Markdown file to HTML
    convert_markdown_to_html(markdown_file, output_file)

    # Exit successfully
    sys.exit(0)
