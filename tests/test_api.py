"""
Test suite for Resume Generator API

Run with: pytest tests/
For tests requiring Docker services: pytest tests/ --with-docker
To run only script tests: pytest tests/ -m "script"
To run only API tests: pytest tests/ -m "api"
"""

import pytest
import requests
import base64
from pathlib import Path
from .conftest import save_content_to_file, validate_pdf_structure


@pytest.mark.api
class TestResumeGeneratorAPI:
    """Test class for Resume Generator API"""

    def test_health_check(self, api_base_url):
        """Test API health check endpoint"""
        response = requests.get(f"{api_base_url}/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Resume Generator"

    def test_root_endpoint(self, api_base_url):
        """Test API root endpoint"""
        response = requests.get(api_base_url)

        assert response.status_code == 200
        data = response.json()
        assert "Resume Generator API" in data["message"]

    def test_generate_resume_success(
        self, api_base_url, api_request_resume, output_dir
    ):
        """Test successful resume generation with PDF validation"""
        response = requests.post(
            f"{api_base_url}/generate-resume", json=api_request_resume, timeout=30
        )

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "message" in data
        assert data["message"] == "Resume generated successfully"
        assert "html_content" in data
        assert "pdf_content" in data

        # Verify content exists
        assert data["html_content"] is not None
        assert data["pdf_content"] is not None
        assert len(data["html_content"]) > 0
        assert len(data["pdf_content"]) > 0

        # Verify HTML content contains expected elements
        html_content = data["html_content"]
        assert "<html" in html_content.lower()
        assert "</html>" in html_content.lower()
        assert "resume" in html_content.lower() or "cv" in html_content.lower()

        # Save files for validation
        html_file = save_content_to_file(
            data["html_content"], "test_resume.html", output_dir
        )
        pdf_file = save_content_to_file(
            data["pdf_content"], "test_resume.pdf", output_dir, is_base64=True
        )

        # Verify files were created
        assert html_file.exists()
        assert pdf_file.exists()
        assert html_file.stat().st_size > 0
        assert pdf_file.stat().st_size > 0

        # Validate PDF structure
        pdf_validation = validate_pdf_structure(pdf_file)

        if pdf_validation["is_valid"] is not None:  # Only if PyPDF is available
            assert pdf_validation[
                "is_valid"
            ], f"PDF validation failed: {pdf_validation['error']}"
            assert pdf_validation["page_count"] > 0, "PDF should have at least one page"
            assert (
                pdf_validation["file_size"] > 1000
            ), "PDF file seems too small to contain meaningful content"

            # Check if PDF has text content (indicates successful rendering)
            if pdf_validation["has_text_content"] is not None:
                assert pdf_validation[
                    "has_text_content"
                ], "PDF should contain extractable text content"

    def test_generate_cover_letter_success(
        self, api_base_url, api_request_cover_letter, output_dir
    ):
        """Test successful cover letter generation with PDF validation"""
        response = requests.post(
            f"{api_base_url}/generate-cover-letter",
            json=api_request_cover_letter,
            timeout=30,
        )

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "message" in data
        assert data["message"] == "Cover letter generated successfully"
        assert "html_content" in data
        assert "pdf_content" in data

        # Verify content exists
        assert data["html_content"] is not None
        assert data["pdf_content"] is not None
        assert len(data["html_content"]) > 0
        assert len(data["pdf_content"]) > 0

        # Verify HTML content contains expected elements
        html_content = data["html_content"]
        assert "<html" in html_content.lower()
        assert "</html>" in html_content.lower()
        assert "cover" in html_content.lower() or "letter" in html_content.lower()

        # Save files for validation
        html_file = save_content_to_file(
            data["html_content"], "test_cover_letter.html", output_dir
        )
        pdf_file = save_content_to_file(
            data["pdf_content"], "test_cover_letter.pdf", output_dir, is_base64=True
        )

        # Verify files were created
        assert html_file.exists()
        assert pdf_file.exists()
        assert html_file.stat().st_size > 0
        assert pdf_file.stat().st_size > 0

        # Validate PDF structure
        pdf_validation = validate_pdf_structure(pdf_file)

        if pdf_validation["is_valid"] is not None:  # Only if PyPDF is available
            assert pdf_validation[
                "is_valid"
            ], f"PDF validation failed: {pdf_validation['error']}"
            assert pdf_validation["page_count"] > 0, "PDF should have at least one page"
            assert (
                pdf_validation["file_size"] > 1000
            ), "PDF file seems too small to contain meaningful content"

            # Check if PDF has text content (indicates successful rendering)
            if pdf_validation["has_text_content"] is not None:
                assert pdf_validation[
                    "has_text_content"
                ], "PDF should contain extractable text content"

    def test_generate_resume_html_only(self, api_base_url, api_request_resume):
        """Test resume generation with HTML only output"""
        request_data = api_request_resume.copy()
        request_data["output_format"] = "html"

        response = requests.post(
            f"{api_base_url}/generate-resume", json=request_data, timeout=30
        )

        assert response.status_code == 200
        data = response.json()

        # Should have HTML but no PDF
        assert data["html_content"] is not None
        assert data["pdf_content"] is None
        assert len(data["html_content"]) > 0

    def test_generate_resume_pdf_only(self, api_base_url, api_request_resume):
        """Test resume generation with PDF only output"""
        request_data = api_request_resume.copy()
        request_data["output_format"] = "pdf"

        response = requests.post(
            f"{api_base_url}/generate-resume", json=request_data, timeout=30
        )

        assert response.status_code == 200
        data = response.json()

        # Should have PDF but no HTML
        assert data["html_content"] is None
        assert data["pdf_content"] is not None
        assert len(data["pdf_content"]) > 0

    def test_generate_resume_invalid_data(self, api_base_url):
        """Test resume generation with invalid data"""
        invalid_data = {
            "resume_data": {},  # Empty resume data
            "personal_info": {},  # Empty personal info
        }

        response = requests.post(
            f"{api_base_url}/generate-resume", json=invalid_data, timeout=30
        )

        # API returns 500 for validation errors in application logic
        assert response.status_code == 500

        # Check that the error message contains validation details
        response_data = response.json()
        assert "detail" in response_data
        assert "validation errors" in response_data["detail"]

    def test_generate_resume_missing_fields(self, api_base_url):
        """Test resume generation with missing required fields"""
        incomplete_data = {
            "resume_data": {"education": []}
            # Missing personal_info
        }

        response = requests.post(
            f"{api_base_url}/generate-resume", json=incomplete_data, timeout=30
        )

        assert response.status_code == 422  # Validation error


@pytest.mark.api
class TestResumeGeneratorIntegration:
    """Integration tests for the Resume Generator API"""

    def test_multiple_concurrent_requests(self, api_base_url, api_request_resume):
        """Test handling multiple concurrent requests"""
        import concurrent.futures
        import threading

        def make_request():
            response = requests.post(
                f"{api_base_url}/generate-resume", json=api_request_resume, timeout=30
            )
            return response.status_code == 200

        # Make 3 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_request) for _ in range(3)]
            results = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

        # All requests should succeed
        assert all(results)

    def test_data_integrity(self, api_base_url, api_request_resume, personal_info_data):
        """Test that generated content contains expected personal information"""
        response = requests.post(
            f"{api_base_url}/generate-resume", json=api_request_resume, timeout=30
        )

        assert response.status_code == 200
        data = response.json()

        html_content = data["html_content"]

        # Check that personal info appears in the HTML
        assert personal_info_data["name"] in html_content
        assert personal_info_data["surname"] in html_content
        assert personal_info_data["email"] in html_content
