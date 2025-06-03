# Markdown to PDF Converter

A Python script that converts markdown files to beautifully formatted PDF documents.

## Features

- Convert single or multiple markdown files to PDF
- Supports advanced markdown features (tables, code blocks, task lists, strikethrough)
- Professional styling with syntax highlighting
- Batch processing capability
- Cross-platform compatibility

## Installation

1. Clone this repository or download the script
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install markdown2 weasyprint
```

## Usage

### Convert a single file:
```bash
python md_to_pdf_converter.py input.md
```

### Convert with custom output name:
```bash
python md_to_pdf_converter.py input.md -o output.pdf
```

### Convert multiple files:
```bash
python md_to_pdf_converter.py *.md
```

### Get help:
```bash
python md_to_pdf_converter.py --help
```

## Requirements

- Python 3.6+
- markdown2
- weasyprint

## Output

The script generates PDF files with:
- Professional typography
- Syntax-highlighted code blocks
- Properly formatted tables
- Styled headers and lists
- Clean margins and spacing

## License

MIT License - feel free to use and modify as needed.