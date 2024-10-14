#!/usr/bin/env python3
import sys
import os
import re
import hashlib

# Function to convert Markdown to HTML (with headings, lists, paragraphs, bold, emphasis, and new transformations)
def markdown_to_html(markdown_content):
    html_lines = []
    in_unordered_list = False
    in_ordered_list = False
    in_paragraph = False
    paragraph_buffer = []

    def close_list_if_open():
        """Close any open list (unordered or ordered)."""
        nonlocal in_unordered_list, in_ordered_list
        if in_unordered_list:
            html_lines.append("</ul>")
            in_unordered_list = False
        if in_ordered_list:
            html_lines.append("</ol>")
            in_ordered_list = False

    def close_paragraph_if_open():
        """Close an open paragraph and flush the buffer."""
        nonlocal in_paragraph, paragraph_buffer
        if in_paragraph:
            # Add line breaks for multi-line text within a paragraph
            for i in range(len(paragraph_buffer)):
                if i > 0:
                    html_lines.append("<br/>")
                html_lines.append(parse_inline_styles(paragraph_buffer[i]))
            html_lines.append("</p>")
            paragraph_buffer = []
            in_paragraph = False

    def md5_hash(content):
        """Convert the content inside [[ ]] to an MD5 hash."""
        return hashlib.md5(content.encode()).hexdigest()

    def remove_letter_c(content):
        """Remove all instances of 'c' (case-insensitive) from the content inside (( ))."""
        return re.sub(r'c', '', content, flags=re.IGNORECASE)

    def parse_inline_styles(text):
        """Parse inline bold, emphasis, MD5, and character removal transformations."""
        # Convert **text** to <b>text</b>
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        # Convert __text__ to <em>text</em>
        text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)
        # Convert [[text]] to MD5 hash
        text = re.sub(r'\[\[(.+?)\]\]', lambda m: md5_hash(m.group(1)), text)
        # Remove all 'c' or 'C' in ((text))
        text = re.sub(r'\(\((.+?)\)\)', lambda m: remove_letter_c(m.group(1)), text)
        return text

    for line in markdown_content.splitlines():
        stripped_line = line.strip()

        # Handle headings
        if stripped_line.startswith('#'):
            close_list_if_open()
            close_paragraph_if_open()
            heading_level = len(stripped_line.split(' ')[0])  # Count number of '#' at the start
            if 1 <= heading_level <= 6:
                heading_text = stripped_line[heading_level:].strip()  # Extract the heading text after the #
                html_lines.append(f"<h{heading_level}>{parse_inline_styles(heading_text)}</h{heading_level}>")
            else:
                html_lines.append(stripped_line)

        # Handle unordered lists (lines starting with '-')
        elif stripped_line.startswith('-'):
            close_paragraph_if_open()
            list_item = stripped_line[1:].strip()  # Remove the '-' and leading spaces
            if not in_unordered_list:
                close_list_if_open()  # Close any open ordered list before starting unordered list
                html_lines.append("<ul>")
                in_unordered_list = True
            html_lines.append(f"<li>{parse_inline_styles(list_item)}</li>")

        # Handle ordered lists (lines starting with '*')
        elif stripped_line.startswith('*'):
            close_paragraph_if_open()
            list_item = stripped_line[1:].strip()  # Remove the '*' and leading spaces
            if not in_ordered_list:
                close_list_if_open()  # Close any open unordered list before starting ordered list
                html_lines.append("<ol>")
                in_ordered_list = True
            html_lines.append(f"<li>{parse_inline_styles(list_item)}</li>")

        # Handle paragraphs
        elif stripped_line:
            close_list_if_open()
            if not in_paragraph:
                html_lines.append("<p>")
                in_paragraph = True
            paragraph_buffer.append(stripped_line)

        # Handle blank lines (used to end paragraphs)
        else:
            close_list_if_open()
            close_paragraph_if_open()

    # Close any open list or paragraph at the end of the file
    close_list_if_open()
    close_paragraph_if_open()

    return '\n'.join(html_lines)

# Main function
def main():
    # Check the number of arguments
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    # Assign the arguments to variables
    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the markdown file exists
    if not os.path.isfile(markdown_file):
        sys.stderr.write(f"Missing {markdown_file}\n")
        sys.exit(1)

    # Process the markdown file and convert to HTML
    try:
        with open(markdown_file, 'r') as md_file:
            markdown_content = md_file.read()

        # Convert markdown to HTML
        html_content = markdown_to_html(markdown_content)

        # Write the converted content to the output HTML file
        with open(output_file, 'w') as html_file:
            html_file.write(html_content)
    
    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)

    # Exit successfully
    sys.exit(0)

# Standard script execution check
if __name__ == "__main__":
    main()
