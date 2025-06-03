#!/usr/bin/env python3
"""
Markdown to PDF Converter (Windows Compatible)

This script converts markdown files to PDF format using markdown2 and reportlab.
Works reliably on Windows without GTK dependencies.

Requirements:
    pip install markdown2 reportlab

Usage:
    python md_to_pdf_converter_windows.py input.md [output.pdf]
    python md_to_pdf_converter_windows.py *.md
"""

import argparse
import sys
import os
from pathlib import Path
import re

try:
    import markdown2
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
except ImportError as e:
    print(f"Missing required package: {e}")
    print("Install with: pip install markdown2 reportlab")
    sys.exit(1)


class MarkdownToPDFConverter:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=20,
            textColor=colors.HexColor('#2c3e50'),
            alignment=TA_LEFT
        ))
        
        # Heading styles
        for i in range(1, 7):
            size = 18 - (i-1) * 2
            space_after = 16 - (i-1) * 2
            self.styles.add(ParagraphStyle(
                name=f'CustomHeading{i}',
                parent=self.styles['Heading1'],
                fontSize=size,
                spaceAfter=space_after,
                spaceBefore=space_after,
                textColor=colors.HexColor('#2c3e50'),
                alignment=TA_LEFT
            ))
        
        # Code style
        self.styles.add(ParagraphStyle(
            name='CustomCode',
            parent=self.styles['Code'],
            fontSize=10,
            fontName='Courier',
            backgroundColor=colors.HexColor('#f8f9fa'),
            borderColor=colors.HexColor('#3498db'),
            borderWidth=1,
            leftIndent=20,
            rightIndent=20,
            spaceAfter=12,
            spaceBefore=12
        ))
        
        # Quote style
        self.styles.add(ParagraphStyle(
            name='CustomQuote',
            parent=self.styles['Normal'],
            fontSize=11,
            leftIndent=30,
            rightIndent=30,
            borderColor=colors.HexColor('#3498db'),
            borderWidth=2,
            textColor=colors.HexColor('#666666'),
            spaceAfter=12,
            spaceBefore=12
        ))

    def clean_html_tags(self, text):
        """Remove HTML tags from text."""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def parse_markdown_to_elements(self, markdown_content):
        """Convert markdown content to reportlab elements."""
        # Convert markdown to HTML first
        html_content = markdown2.markdown(
            markdown_content,
            extras=['fenced-code-blocks', 'tables', 'strike', 'task_list']
        )
        
        elements = []
        lines = html_content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                i += 1
                continue
            
            # Handle headings
            if line.startswith('<h1>'):
                text = self.clean_html_tags(line)
                elements.append(Paragraph(text, self.styles['CustomHeading1']))
                elements.append(Spacer(1, 12))
            
            elif line.startswith('<h2>'):
                text = self.clean_html_tags(line)
                elements.append(Paragraph(text, self.styles['CustomHeading2']))
                elements.append(Spacer(1, 10))
            
            elif line.startswith('<h3>'):
                text = self.clean_html_tags(line)
                elements.append(Paragraph(text, self.styles['CustomHeading3']))
                elements.append(Spacer(1, 8))
            
            elif line.startswith('<h4>'):
                text = self.clean_html_tags(line)
                elements.append(Paragraph(text, self.styles['CustomHeading4']))
                elements.append(Spacer(1, 6))
            
            elif line.startswith('<h5>'):
                text = self.clean_html_tags(line)
                elements.append(Paragraph(text, self.styles['CustomHeading5']))
                elements.append(Spacer(1, 4))
            
            elif line.startswith('<h6>'):
                text = self.clean_html_tags(line)
                elements.append(Paragraph(text, self.styles['CustomHeading6']))
                elements.append(Spacer(1, 4))
            
            # Handle code blocks
            elif line.startswith('<pre><code>'):
                code_lines = []
                if line.endswith('</code></pre>'):
                    # Single line code block
                    code_text = self.clean_html_tags(line)
                    elements.append(Preformatted(code_text, self.styles['CustomCode']))
                else:
                    # Multi-line code block
                    code_lines.append(self.clean_html_tags(line))
                    i += 1
                    while i < len(lines) and not lines[i].strip().endswith('</code></pre>'):
                        code_lines.append(lines[i])
                        i += 1
                    if i < len(lines):
                        code_lines.append(self.clean_html_tags(lines[i]))
                    
                    code_text = '\n'.join(code_lines)
                    elements.append(Preformatted(code_text, self.styles['CustomCode']))
                elements.append(Spacer(1, 12))
            
            # Handle blockquotes
            elif line.startswith('<blockquote>'):
                quote_lines = []
                if line.endswith('</blockquote>'):
                    # Single line quote
                    quote_text = self.clean_html_tags(line)
                    elements.append(Paragraph(quote_text, self.styles['CustomQuote']))
                else:
                    # Multi-line quote
                    quote_lines.append(self.clean_html_tags(line))
                    i += 1
                    while i < len(lines) and not lines[i].strip().endswith('</blockquote>'):
                        quote_lines.append(self.clean_html_tags(lines[i]))
                        i += 1
                    if i < len(lines):
                        quote_lines.append(self.clean_html_tags(lines[i]))
                    
                    quote_text = ' '.join(quote_lines)
                    elements.append(Paragraph(quote_text, self.styles['CustomQuote']))
                elements.append(Spacer(1, 12))
            
            # Handle tables
            elif line.startswith('<table>'):
                table_data = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('</table>'):
                    row_line = lines[i].strip()
                    if row_line.startswith('<tr>'):
                        row_data = []
                        cells = re.findall(r'<t[hd]>(.*?)</t[hd]>', row_line)
                        for cell in cells:
                            row_data.append(self.clean_html_tags(cell))
                        if row_data:
                            table_data.append(row_data)
                    i += 1
                
                if table_data:
                    table = Table(table_data)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f2f2f2')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    elements.append(table)
                    elements.append(Spacer(1, 12))
            
            # Handle regular paragraphs
            elif line.startswith('<p>'):
                text = self.clean_html_tags(line)
                if text.strip():
                    elements.append(Paragraph(text, self.styles['Normal']))
                    elements.append(Spacer(1, 6))
            
            # Handle list items
            elif line.startswith('<li>'):
                text = self.clean_html_tags(line)
                elements.append(Paragraph(f"• {text}", self.styles['Normal']))
                elements.append(Spacer(1, 3))
            
            # Handle other content
            else:
                text = self.clean_html_tags(line)
                if text.strip():
                    elements.append(Paragraph(text, self.styles['Normal']))
                    elements.append(Spacer(1, 6))
            
            i += 1
        
        return elements

    def convert_markdown_to_pdf(self, markdown_file, output_file=None):
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
        
        # Determine output filename
        if output_file is None:
            output_file = Path(markdown_file).with_suffix('.pdf')
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                str(output_file),
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Convert markdown to elements
            elements = self.parse_markdown_to_elements(markdown_content)
            
            # Build PDF
            doc.build(elements)
            
            print(f"Successfully converted '{markdown_file}' to '{output_file}'")
            return True
            
        except Exception as e:
            print(f"Error converting '{markdown_file}' to PDF: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert markdown files to PDF format (Windows compatible)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python md_to_pdf_converter_windows.py README.md
    python md_to_pdf_converter_windows.py README.md output.pdf
    python md_to_pdf_converter_windows.py *.md
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
    
    converter = MarkdownToPDFConverter()
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
        
        if converter.convert_markdown_to_pdf(markdown_file, output_file):
            success_count += 1
    
    print(f"\nConversion complete: {success_count}/{total_count} files processed successfully.")
    
    if success_count == 0:
        sys.exit(1)


if __name__ == '__main__':
    main()