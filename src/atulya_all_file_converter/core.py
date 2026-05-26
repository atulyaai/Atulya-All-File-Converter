import os
import csv
import json
import io
from xml.etree import ElementTree as ET

from .utils import IMAGE_EXTENSIONS, detect_format, get_compatible_formats, ensure_output_dir, format_size


def convert_file(input_path, output_path, quality=90, page_range=None):
    input_format = detect_format(input_path)
    output_ext = os.path.splitext(output_path.lower())[1]
    output_format = detect_format(output_path)

    if not input_format:
        raise ValueError(f"Unsupported input format: {input_path}")

    if not output_format:
        raise ValueError(f"Unsupported output format: {output_path}")

    compatible = get_compatible_formats(input_format)
    if output_format not in compatible and input_format not in ["jpg", "png"] and output_format not in ["jpg", "png"]:
        if input_format not in IMAGE_EXTENSIONS and output_format not in IMAGE_EXTENSIONS:
            raise ValueError(f"Cannot convert {input_format} to {output_format}")

    ensure_output_dir(output_path)

    if input_format in ("csv", "xlsx") and output_format in ("csv", "xlsx", "json", "html", "xml"):
        _convert_spreadsheet(input_path, output_path)
    elif input_format in ("json",) and output_format in ("csv", "xlsx", "xml", "html"):
        _convert_json(input_path, output_path)
    elif input_format in ("xml",) and output_format in ("json", "csv", "xlsx"):
        _convert_xml(input_path, output_path)
    elif input_format in ("html", "txt") and output_format in ("txt", "html"):
        _convert_text(input_path, output_path)
    elif input_format in IMAGE_EXTENSIONS or output_format in IMAGE_EXTENSIONS:
        _convert_image(input_path, output_path, quality)
    elif input_format == "pdf" and output_format in ("txt", "html"):
        _convert_pdf_text(input_path, output_path)
    else:
        raise ValueError(f"Conversion from {input_format} to {output_format} not implemented")

    return format_size(os.path.getsize(output_path))


def _convert_spreadsheet(input_path, output_path):
    import pandas as pd

    ext = os.path.splitext(input_path.lower())[1]
    if ext == ".csv":
        df = pd.read_csv(input_path)
    else:
        df = pd.read_excel(input_path, engine="openpyxl")

    out_ext = os.path.splitext(output_path.lower())[1]
    if out_ext == ".csv":
        df.to_csv(output_path, index=False)
    elif out_ext in (".xlsx", ".xls"):
        df.to_excel(output_path, index=False, engine="xlsxwriter")
    elif out_ext == ".json":
        df.to_json(output_path, orient="records", indent=2)
    elif out_ext == ".html":
        df.to_html(output_path, index=False)
    elif out_ext == ".xml":
        df.to_xml(output_path, index=False)


def _convert_json(input_path, output_path):
    import pandas as pd

    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame([data])

    out_ext = os.path.splitext(output_path.lower())[1]
    if out_ext == ".csv":
        df.to_csv(output_path, index=False)
    elif out_ext in (".xlsx", ".xls"):
        df.to_excel(output_path, index=False, engine="xlsxwriter")
    elif out_ext == ".xml":
        df.to_xml(output_path, index=False)
    elif out_ext == ".html":
        df.to_html(output_path, index=False)


def _convert_xml(input_path, output_path):
    import pandas as pd

    tree = ET.parse(input_path)
    root = tree.getroot()
    records = []
    for child in root:
        record = {}
        for sub in child:
            record[sub.tag] = sub.text
        records.append(record)

    df = pd.DataFrame(records) if records else pd.DataFrame()
    out_ext = os.path.splitext(output_path.lower())[1]
    if out_ext == ".json":
        df.to_json(output_path, orient="records", indent=2)
    elif out_ext == ".csv":
        df.to_csv(output_path, index=False)
    elif out_ext in (".xlsx", ".xls"):
        df.to_excel(output_path, index=False, engine="xlsxwriter")


def _convert_text(input_path, output_path):
    with open(input_path, encoding="utf-8", errors="replace") as f:
        content = f.read()

    out_ext = os.path.splitext(output_path.lower())[1]
    if out_ext == ".txt":
        import html
        content = html.unescape(content)
        content = content.replace("<br>", "\n").replace("<br/>", "\n").replace("</p>", "\n\n")
        content = content.replace("<div>", "").replace("</div>", "\n")
        import re
        content = re.sub(r"<[^>]+>", "", content)
        content = "\n".join(line.strip() for line in content.splitlines() if line.strip())
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    elif out_ext == ".html":
        content = content.replace("\n", "<br>\n")
        html_content = f"<!DOCTYPE html><html><body><pre>{content}</pre></body></html>"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)


def _convert_image(input_path, output_path, quality):
    from PIL import Image

    img = Image.open(input_path)
    out_ext = os.path.splitext(output_path.lower())[1]

    if img.mode == "RGBA" and out_ext in (".jpg", ".jpeg"):
        img = img.convert("RGB")

    save_kwargs = {}
    if out_ext in (".jpg", ".jpeg"):
        save_kwargs["quality"] = quality
    elif out_ext == ".png":
        save_kwargs["compress_level"] = max(0, 9 - quality // 11)

    if out_ext == ".pdf":
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(output_path, "PDF", resolution=100)
    else:
        img.save(output_path, **save_kwargs)


def _convert_pdf_text(input_path, output_path):
    raise NotImplementedError("PDF text conversion requires PyMuPDF (pip install atulya-convert[pdf])")


def get_file_info(filepath):
    import datetime

    stat = os.stat(filepath)
    fmt = detect_format(filepath)
    info = {
        "path": filepath,
        "size": format_size(stat.st_size),
        "format": fmt or "unknown",
        "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
    }

    ext = os.path.splitext(filepath.lower())[1]
    if ext in IMAGE_EXTENSIONS:
        from PIL import Image
        img = Image.open(filepath)
        info["dimensions"] = f"{img.width}x{img.height}"
        info["mode"] = img.mode

    return info


def batch_convert(input_dir, pattern, output_dir, output_format, quality=90):
    import glob
    import os

    matched = glob.glob(os.path.join(input_dir, pattern))
    results = []
    for input_path in matched:
        base = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_dir, f"{base}.{output_format}")
        try:
            result = convert_file(input_path, output_path, quality)
            results.append((base, "ok", result))
        except Exception as e:
            results.append((base, "error", str(e)))
    return results


def merge_images_to_pdf(input_paths, output_path):
    from PIL import Image

    images = []
    for path in input_paths:
        img = Image.open(path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        images.append(img)

    if images:
        images[0].save(output_path, "PDF", save_all=True, append_images=images[1:], resolution=100)
        return format_size(os.path.getsize(output_path))
    raise ValueError("No images to merge")


def split_pdf_to_images(input_path, output_dir, page_range=None):
    raise NotImplementedError("PDF splitting requires PyMuPDF (pip install atulya-convert[pdf])")


def compress_image(input_path, output_path, quality=70, max_width=None):
    from PIL import Image

    img = Image.open(input_path)
    if max_width and img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)

    if img.mode == "RGBA":
        img = img.convert("RGB")

    img.save(output_path, quality=quality, optimize=True)
    return format_size(os.path.getsize(output_path))
