#!/usr/bin/env python3
"""
Markdown to PDF Converter

This script converts markdown files to PDF format using markdown2 and weasyprint.
Supports multiple markdown files and preserves formatting.

Requirements:
    pip install markdown2 weasyprint

Usage:
    python md_to_pdf_converter.py input.md [output.pdf]
    python md_to_pdf_converter.py *.md
"""

import argparse
import sys
import os
from pathlib import Path

try:
    import markdown2
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
except ImportError as e:
    print(f"Missing required package: {e}")
    print("Install with: pip install markdown2 weasyprint")
    sys.exit(1)


def convert_markdown_to_pdf(markdown_file, output_file=None):
    """Convert a single markdown file to PDF."""
    
    # Read markdown file
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{markdown_file}' not found.")
        return False
    except Exception as e:
        print(f"Error reading '{markdown_file}': {e}")
        return False
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(
        markdown_content,
        extras=['fenced-code-blocks', 'tables', 'strike', 'task_list']
    )
    
    # Add basic CSS styling
    css_style = """
    <style>
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            margin: 40px;
            color: #333;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 24px;
            margin-bottom: 16px;
        }
        h1 { font-size: 2em; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        h2 { font-size: 1.5em; border-bottom: 1px solid #bdc3c7; padding-bottom: 8px; }
        code {
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background-color: #f8f9fa;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }
        pre code {
            background-color: transparent;
            padding: 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 16px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        blockquote {
            border-left: 4px solid #3498db;
            margin: 16px 0;
            padding-left: 16px;
            color: #666;
        }
        ul, ol {
            padding-left: 24px;
        }
        li {
            margin-bottom: 4px;
        }
    </style>
    """
    
    # Create complete HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{Path(markdown_file).stem}</title>
        {css_style}
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Determine output filename
    if output_file is None:
        output_file = Path(markdown_file).with_suffix('.pdf')
    
    # Convert HTML to PDF
    try:
        font_config = FontConfiguration()
        html_doc = HTML(string=full_html)
        css_doc = CSS(string='@page { margin: 2cm; }')
        
        html_doc.write_pdf(
            output_file,
            stylesheets=[css_doc],
            font_config=font_config
        )
        
        print(f"Successfully converted '{markdown_file}' to '{output_file}'")
        return True
        
    except Exception as e:
        print(f"Error converting '{markdown_file}' to PDF: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert markdown files to PDF format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python md_to_pdf_converter.py README.md
    python md_to_pdf_converter.py README.md output.pdf
    python md_to_pdf_converter.py *.md
        """
    )
    
    parser.add_argument(
        'input_files',
        nargs='+',
        help='Markdown file(s) to convert'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output PDF file (only for single input file)'
    )
    
    args = parser.parse_args()
    
    # Check if output is specified with multiple input files
    if len(args.input_files) > 1 and args.output:
        print("Error: Cannot specify output filename with multiple input files.")
        sys.exit(1)
    
    success_count = 0
    total_count = len(args.input_files)
    
    for markdown_file in args.input_files:
        if not os.path.exists(markdown_file):
            print(f"Warning: File '{markdown_file}' does not exist. Skipping.")
            continue
            
        if not markdown_file.lower().endswith(('.md', '.markdown')):
            print(f"Warning: '{markdown_file}' doesn't appear to be a markdown file. Skipping.")
            continue
        
        output_file = args.output if args.output else None
        
        if convert_markdown_to_pdf(markdown_file, output_file):
            success_count += 1
    
    print(f"\nConversion complete: {success_count}/{total_count} files processed successfully.")
    
    if success_count == 0:
        sys.exit(1)


if __name__ == '__main__':
    main()