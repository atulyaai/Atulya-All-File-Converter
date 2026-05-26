import os
import sys
import glob as globmod

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

from . import __version__
from .core import convert_file, get_file_info, batch_convert, merge_images_to_pdf, compress_image
from .utils import SUPPORTED_FORMATS, format_size

console = Console()


@click.group()
@click.version_option(__version__)
def main():
    pass


@main.command()
@click.option("-i", "--input", required=True, help="Input file path")
@click.option("-o", "--output", required=True, help="Output file path")
@click.option("-q", "--quality", default=90, type=int, help="Quality for image conversion (1-100)")
@click.option("-p", "--page", default=None, help="Page range for PDF (e.g., 1-5)")
def convert(input, output, quality, page):
    result = convert_file(input, output, quality, page)
    console.print(f"[green]Converted:[/] {input} -> {output} [dim]({result})[/dim]")


@main.group()
def batch():
    pass


@batch.command()
@click.option("-i", "--input-dir", required=True, help="Input directory")
@click.option("--pattern", default="*.*", help="File glob pattern")
@click.option("-o", "--output-dir", required=True, help="Output directory")
@click.option("--format", "output_format", required=True, help="Output format (extension)")
@click.option("-q", "--quality", default=90, type=int)
def convert(input_dir, pattern, output_dir, output_format, quality):
    os.makedirs(output_dir, exist_ok=True)
    results = batch_convert(input_dir, pattern, output_dir, output_format, quality)
    table = Table(title="Batch Conversion Results")
    table.add_column("File")
    table.add_column("Status")
    table.add_column("Result")
    for name, status, detail in results:
        style = "green" if status == "ok" else "red"
        table.add_row(name, status, detail, style=style)
    console.print(table)


@batch.command()
@click.option("-i", "--input", "input_pattern", required=True, help="Input images glob (e.g., *.jpg)")
@click.option("-o", "--output", required=True, help="Output PDF path")
def merge(input_pattern, output):
    files = sorted(globmod.glob(input_pattern))
    if not files:
        console.print("[red]No files matched pattern[/red]")
        sys.exit(1)
    result = merge_images_to_pdf(files, output)
    console.print(f"[green]Merged {len(files)} images to[/] {output} [dim]({result})[/dim]")



@main.group()
def info():
    pass


@info.command()
@click.argument("filepath")
def file(filepath):
    info_dict = get_file_info(filepath)
    table = Table(title=f"File Info: {os.path.basename(filepath)}")
    table.add_column("Property")
    table.add_column("Value")
    for key, val in info_dict.items():
        table.add_row(key, str(val))
    console.print(table)


@info.command()
def formats():
    table = Table(title="Supported Conversions")
    table.add_column("Input Format")
    table.add_column("Output Formats")
    for fmt, info_dict in sorted(SUPPORTED_FORMATS.items()):
        table.add_row(fmt, ", ".join(info_dict["convertible_to"]))
    console.print(table)


@main.group()
def compress():
    pass


@compress.command()
@click.option("-i", "--input", required=True, help="Input image path")
@click.option("-o", "--output", required=True, help="Output image path")
@click.option("-q", "--quality", default=70, type=int, help="JPEG quality (1-100)")
@click.option("--max-width", default=None, type=int, help="Resize to max width")
def images(input, output, quality, max_width):
    result = compress_image(input, output, quality, max_width)
    before = format_size(os.path.getsize(input))
    console.print(f"[green]Compressed:[/] {input} -> {output} [dim]({before} -> {result})[/dim]")
