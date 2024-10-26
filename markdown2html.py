#!/usr/bin/python3
"""
Markdown to HTML converter script that parses headings, unordered lists, ordered lists, paragraphs, bold, and italic text.
"""

import sys
import os
import re

def convert_markdown_to_html(markdown_file: str, output_file: str) -> None:
    """Converts Markdown headings, lists, paragraphs, bold, and italic text to HTML and writes to an output file."""
    with open(markdown_file, 'r') as md_file, open(output_file, 'w') as html_file:
        inside_unordered_list = False  # Track if we are currently inside an unordered list
        inside_ordered_list = False    # Track if we are currently inside an ordered list
        paragraph_lines = []            # Store lines for the current paragraph

        for line in md_file:
            line = line.rstrip()  # Remove trailing whitespace
            
            # Check for headings
            if line.startswith('#'):
                if inside_unordered_list:
                    html_file.write("</ul>\n")  # Close unordered list if open
                    inside_unordered_list = False
                if inside_ordered_list:
                    html_file.write("</ol>\n")   # Close ordered list if open
                    inside_ordered_list = False
                
                heading_level = line.count('#')
                heading_text = line[heading_level:].strip()
                if 1 <= heading_level <= 6:  # Ensure heading level is valid
                    html_file.write(f"<h{heading_level}>{heading_text}</h{heading_level}>\n")
                continue
            
            # Check for unordered lists
            if line.startswith('- '):
                if not inside_unordered_list:  # Start a new unordered list
                    html_file.write("<ul>\n")
                    inside_unordered_list = True
                list_item = line[2:].strip()  # Get the item text after '- '
                html_file.write(f"  <li>{parse_bold_italic(list_item)}</li>\n")
                continue
            
            # Check for ordered lists
            if line.startswith('* '):
                if not inside_ordered_list:  # Start a new ordered list
                    html_file.write("<ol>\n")
                    inside_ordered_list = True
                list_item = line[2:].strip()  # Get the item text after '* '
                html_file.write(f"  <li>{parse_bold_italic(list_item)}</li>\n")
                continue
            
            # Handle paragraphs
            if line.strip() == "":
                if paragraph_lines:  # If we have collected paragraph lines, write them out
                    html_file.write("<p>\n")
                    html_file.write("<br />\n".join(paragraph_lines))
                    html_file.write("</p>\n")
                    paragraph_lines.clear()  # Clear collected lines for the next paragraph
            else:
                paragraph_lines.append(parse_bold_italic(line.strip()))  # Add line to the current paragraph

        # Close any open lists and remaining paragraph at the end of the file
        if inside_unordered_list:
            html_file.write("</ul>\n")
        if inside_ordered_list:
            html_file.write("</ol>\n")
        if paragraph_lines:  # Write the last paragraph if any lines are left
            html_file.write("<p>\n")
            html_file.write("<br />\n".join(paragraph_lines))
            html_file.write("</p>\n")

def parse_bold_italic(text: str) -> str:
    """Parses bold and italic syntax in the text."""
    # Replace bold syntax **text** with <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Replace italic syntax __text__ with <em>text</em>
    text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)
    return text

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

