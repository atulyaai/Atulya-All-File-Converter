import os
import platform

SUPPORTED_FORMATS = {
    "csv": {"extensions": [".csv"], "convertible_to": ["xlsx", "json", "html", "sql"]},
    "xlsx": {"extensions": [".xlsx", ".xls"], "convertible_to": ["csv", "json", "html", "xml"]},
    "json": {"extensions": [".json"], "convertible_to": ["csv", "xlsx", "xml", "html"]},
    "xml": {"extensions": [".xml"], "convertible_to": ["json", "csv", "xlsx"]},
    "html": {"extensions": [".html", ".htm"], "convertible_to": ["pdf", "txt", "docx"]},
    "txt": {"extensions": [".txt"], "convertible_to": ["html", "csv", "json"]},
    "jpg": {"extensions": [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tiff"], "convertible_to": ["pdf", "png", "jpg", "webp", "bmp"]},
    "png": {"extensions": [".png"], "convertible_to": ["pdf", "jpg", "webp", "bmp"]},
    "pdf": {"extensions": [".pdf"], "convertible_to": ["jpg", "png", "txt", "html"]},
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tiff"}
DOCUMENT_EXTENSIONS = {".pdf", ".docx", ".doc"}


def detect_format(filepath):
    _, ext = os.path.splitext(filepath.lower())
    for fmt, info in SUPPORTED_FORMATS.items():
        if ext in info["extensions"]:
            return fmt
    return None


def get_compatible_formats(input_format):
    info = SUPPORTED_FORMATS.get(input_format)
    if info:
        return info["convertible_to"]
    return []


def format_size(bytes_val):
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} TB"


def ensure_output_dir(path):
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)


def get_output_path(input_path, output_ext):
    base = os.path.splitext(input_path)[0]
    return base + output_ext


def parse_page_range(page_str, total_pages):
    if not page_str:
        return list(range(total_pages))
    pages = []
    for part in page_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            pages.extend(range(int(start) - 1, int(end)))
        else:
            pages.append(int(part) - 1)
    return [p for p in pages if 0 <= p < total_pages]
