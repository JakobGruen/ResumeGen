import subprocess
import os
import requests
from pathlib import Path

PDF_SERVICE_PATH = Path(__file__).parent.parent / "PdfService"


def generate_pdf_http(html_content: str, pdf_path: Path | str, pdf_service_url: str):
    """
    Generate PDF using HTTP PDF service.
    Args:
        html_content (str): HTML content to convert to PDF.
        pdf_path (str): Path to save the output PDF file.
        pdf_service_url (str): URL of the PDF service (e.g., 'http://pdf-service:3000').
    """
    try:
        response = requests.post(
            f"{pdf_service_url}/generate-pdf", json={"html": html_content}, timeout=60
        )
        response.raise_for_status()

        # Save the PDF content
        with open(pdf_path, "wb") as f:
            f.write(response.content)

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"HTTP PDF generation failed: {e}")


def generate_pdf_subprocess(
    html_path: Path | str,
    pdf_path: Path | str,
    node_script_path: Path | str | None = None,
):
    """
    Generate PDF using subprocess (CLI method).
    Args:
        html_path (str): Path to the input HTML file.
        pdf_path (str): Path to the output PDF file.
        node_script_path (str, optional): Path to the Node.js script.
    """
    if node_script_path is None:
        node_script_path = PDF_SERVICE_PATH / "index.js"

    # Ensure absolute paths
    node_script_path = Path(node_script_path).resolve()
    html_path = Path(html_path).resolve()
    pdf_path = Path(pdf_path).resolve()

    result = subprocess.run(
        ["node", node_script_path, html_path, pdf_path], capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"PDF generation failed: {result.stderr}")


def generate_pdf(
    html_path: Path | str,
    pdf_path: Path | str,
    node_script_path: Path | str | None = None,
):
    """
    Calls the Node.js Puppeteer script to generate a PDF from an HTML file.
    Automatically detects whether to use HTTP service or subprocess based on environment.
    Args:
        html_path (str): Path to the input HTML file.
        pdf_path (str): Path to the output PDF file.
        node_script_path (str, optional): Path to the generate_pdf.js script. Defaults to '../pdf_service/generate_pdf.js'.
    Returns:
        str: Path to the generated PDF file.
    Raises:
        RuntimeError: If PDF generation fails.
    """
    # Check if PDF_SERVICE_URL environment variable is set (microservices mode)
    pdf_service_url = os.getenv("PDF_SERVICE_URL")

    if pdf_service_url:
        # Use HTTP service
        html_path = Path(html_path)
        try:
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            generate_pdf_http(html_content, pdf_path, pdf_service_url)
        except FileNotFoundError:
            raise RuntimeError(f"HTML file not found: {html_path}")
    else:
        # Use subprocess (CLI method)
        generate_pdf_subprocess(html_path, pdf_path, node_script_path)
