"""
Pytest configuration and fixtures for Resume Generator API tests
"""

import pytest
import json
import requests
import base64
import tempfile
import shutil
import subprocess
import time
import os
from pathlib import Path
from typing import Dict, Any

try:
    from pypdf import PdfReader

    PDF_VALIDATION_AVAILABLE = True
except ImportError:
    PDF_VALIDATION_AVAILABLE = False


def pytest_addoption(parser):
    """Add command line options for pytest"""
    parser.addoption(
        "--with-docker",
        action="store_true",
        default=False,
        help="Automatically start/stop Docker Compose services for API tests",
    )


@pytest.fixture(scope="session")
def docker_compose_services(request):
    """
    Manage Docker Compose services for API tests.
    Only starts services if --with-docker flag is used.
    """
    if not request.config.getoption("--with-docker"):
        # Skip Docker management, assume services are running
        yield
        return

    project_root = Path(__file__).parent.parent
    compose_file = project_root / "docker-compose.yml"

    if not compose_file.exists():
        pytest.skip("docker-compose.yml not found")

    # Check if docker-compose is available
    compose_cmd = None
    try:
        # Try modern Docker Desktop command first
        subprocess.run(
            ["docker", "compose", "version"], capture_output=True, check=True
        )
        compose_cmd = ["docker", "compose"]
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Fallback to legacy docker-compose
            subprocess.run(
                ["docker-compose", "--version"], capture_output=True, check=True
            )
            compose_cmd = ["docker-compose"]
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("Docker Compose not available")

    # Start services
    print("\n🐳 Starting Docker Compose services...")
    try:
        result = subprocess.run(
            compose_cmd + ["-f", str(compose_file), "up", "-d", "--build"],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True,
        )

        # Wait for services to be healthy
        print("⏳ Waiting for services to be ready...")
        wait_for_service("http://localhost:8000/health", timeout=60)
        wait_for_service("http://localhost:3000/health", timeout=60)
        print("✅ Services are ready!")

        yield

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Docker services:")
        print(f"Command: {' '.join(e.cmd)}")
        print(f"Return code: {e.returncode}")
        if e.stdout:
            print(f"STDOUT:\n{e.stdout}")
        if e.stderr:
            print(f"STDERR:\n{e.stderr}")

        # Try to get more details with docker-compose logs
        try:
            logs_result = subprocess.run(
                compose_cmd + ["-f", str(compose_file), "logs"],
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=10,
            )
            if logs_result.stdout:
                print(f"Docker Compose Logs:\n{logs_result.stdout}")
        except:
            pass

        pytest.skip(f"Failed to start Docker services: {e}")

    finally:
        # Stop services
        print("\n🛑 Stopping Docker Compose services...")
        subprocess.run(
            compose_cmd + ["-f", str(compose_file), "down"],
            cwd=project_root,
            capture_output=True,
        )


def wait_for_service(url: str, timeout: int = 30, interval: float = 1.0):
    """Wait for a service to become available"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(interval)

    raise TimeoutError(
        f"Service at {url} did not become available within {timeout} seconds"
    )


@pytest.fixture(scope="session")
def api_base_url(docker_compose_services):
    """Base URL for the API - depends on Docker services if enabled"""
    return "http://localhost:8000"


@pytest.fixture(scope="session")
def test_data_dir():
    """Path to test data directory"""
    return Path(__file__).parent.parent / "data"


@pytest.fixture(scope="session")
def resume_data(test_data_dir):
    """Load resume test data"""
    with open(test_data_dir / "resume_example.json", "r") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def personal_info_data(test_data_dir):
    """Load personal info test data"""
    with open(test_data_dir / "personal_info_example.json", "r") as f:
        data = json.load(f)
        return data


@pytest.fixture(scope="session")
def cover_letter_data(test_data_dir):
    """Load cover letter test data"""
    with open(test_data_dir / "cover_letter_example.json", "r") as f:
        return json.load(f)


@pytest.fixture
def api_request_resume(resume_data, personal_info_data):
    """Resume API request data"""
    return {
        "resume_data": resume_data,
        "personal_info": personal_info_data,
        "output_format": "both",
    }


@pytest.fixture
def api_request_cover_letter(cover_letter_data, personal_info_data):
    """Cover letter API request data"""
    return {
        "cover_letter_data": cover_letter_data,
        "personal_info": personal_info_data,
        "output_format": "both",
    }


@pytest.fixture
def output_dir():
    """Output directory for test files - automatically cleaned up after tests"""
    temp_dir = tempfile.mkdtemp(prefix="resumegen_test_")
    output_path = Path(temp_dir)
    yield output_path
    # Cleanup after test
    shutil.rmtree(output_path, ignore_errors=True)


def save_content_to_file(
    content: str, filename: str, output_dir: Path, is_base64: bool = False
):
    """Helper function to save content to file"""
    filepath = output_dir / filename

    if is_base64:
        # Decode base64 content and save as binary
        content_bytes = base64.b64decode(content)
        with open(filepath, "wb") as f:
            f.write(content_bytes)
    else:
        # Save as text
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return filepath


def validate_pdf_structure(pdf_path: Path) -> Dict[str, Any]:
    """
    Validate PDF file structure and return metadata

    Returns:
        dict: Contains validation results and metadata
    """
    if not PDF_VALIDATION_AVAILABLE:
        return {
            "is_valid": None,
            "error": "PyPDF not available for validation",
            "page_count": None,
            "metadata": None,
        }

    try:
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)

            # Basic validation
            page_count = len(reader.pages)
            metadata = reader.metadata

            # Try to read first page to ensure PDF is readable
            if page_count > 0:
                first_page = reader.pages[0]
                # Try to extract text to ensure page is valid
                text_content = first_page.extract_text()
                has_text = len(text_content.strip()) > 0
            else:
                has_text = False

            return {
                "is_valid": True,
                "page_count": page_count,
                "has_text_content": has_text,
                "metadata": dict(metadata) if metadata else None,
                "file_size": pdf_path.stat().st_size,
                "error": None,
            }

    except Exception as e:
        return {
            "is_valid": False,
            "error": str(e),
            "page_count": None,
            "metadata": None,
            "file_size": pdf_path.stat().st_size if pdf_path.exists() else 0,
        }
