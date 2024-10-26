#!/usr/bin/python3
"""
Markdown to HTML converter script that parses headings and unordered lists.
"""

import sys
import os

def convert_markdown_to_html(markdown_file: str, output_file: str) -> None:
    """Converts Markdown headings and unordered lists to HTML and writes to an output file."""
    with open(markdown_file, 'r') as md_file, open(output_file, 'w') as html_file:
        inside_list = False  # Track if we are currently inside an unordered list

        for line in md_file:
            line = line.rstrip()  # Remove trailing whitespace
            
            # Check for headings
            if line.startswith('#'):
                heading_level = line.count('#')
                heading_text = line[heading_level:].strip()
                if 1 <= heading_level <= 6:  # Ensure heading level is valid
                    if inside_list:
                        html_file.write("</ul>\n")  # Close any open unordered list
                        inside_list = False
                    html_file.write(f"<h{heading_level}>{heading_text}</h{heading_level}>\n")
                    continue
            
            # Check for unordered lists
            if line.startswith('- '):
                if not inside_list:  # Start a new unordered list
                    html_file.write("<ul>\n")
                    inside_list = True
                list_item = line[2:].strip()  # Get the item text after '- '
                html_file.write(f"  <li>{list_item}</li>\n")
            else:
                if inside_list:  # Close any open unordered list if a non-list line is encountered
                    html_file.write("</ul>\n")
                    inside_list = False
        
        # Close any open unordered list at the end of the file
        if inside_list:
            html_file.write("</ul>\n")

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
