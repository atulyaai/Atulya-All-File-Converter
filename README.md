# Atulya All File Converter

Private offline PDF, image, document and media converter — any file to any format.

## Supported Conversions

| From | To |
|------|----|
| PDF | DOCX, XLSX, CSV, Images, HTML, Text |
| DOCX/DOC | PDF, Text, HTML, Images |
| XLSX/XLS | PDF, CSV, JSON, XML |
| Images (JPG, PNG, WEBP, BMP) | PDF, Each other format |
| CSV/TSV | XLSX, JSON, SQL, HTML |
| HTML | PDF, DOCX, Text |
| JSON/XML | CSV, XLSX |

## Quick Start

```bash
pip install atulya-all-file-converter

# Convert PDF to DOCX
atulya-convert invoice.pdf invoice.docx

# Batch convert images to PDF
atulya-convert batch --input *.jpg --output scans.pdf

# Convert Excel to JSON
atulya-convert data.xlsx data.json
```

## Features

- 100% offline — no data leaves your machine
- Batch conversion with progress bars
- Preserve formatting where possible
- CLI and Python API
- Drag-drop GUI (optional)

## License

MIT
