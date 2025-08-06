"""
Test suite for Resume Generator CLI Script

Run with: pytest tests/test_script.py -m "script"
"""

import pytest
from pathlib import Path
from .conftest import validate_pdf_structure
from resumegen.cli import generate_resume, generate_cover_letter


@pytest.mark.cli
class TestResumeGeneratorScript:
    """Test class for Resume Generator CLI Script"""

    def test_generate_resume(self, test_data_dir: Path):
        """Test resume generation using default paths"""
        resume_path = (test_data_dir / "resume_example.json").resolve()
        info_path = (test_data_dir / "personal_info_example.json").resolve()
        out_html = (test_data_dir / "resume_example.html").resolve()
        out_pdf = (test_data_dir / "resume_example.pdf").resolve()

        generate_resume(
            resume_path=str(resume_path),
            info_path=str(info_path),
            out_html=str(out_html),
            out_pdf=str(out_pdf),
        )

        assert out_html.exists()
        assert out_pdf.exists()

        # Validate HTML content
        html_content = out_html.read_text()
        assert len(html_content) > 100
        assert "<html" in html_content

        # Validate PDF structure
        validate_pdf_structure(out_pdf)

        # Clean up generated files
        out_html.unlink()
        out_pdf.unlink()

    def test_generate_cover_letter(self, test_data_dir: Path):
        """Test cover letter generation"""
        letter_path = (test_data_dir / "cover_letter_example.json").resolve()
        info_path = (test_data_dir / "personal_info_example.json").resolve()
        out_html = (test_data_dir / "cover_letter_example.html").resolve()
        out_pdf = (test_data_dir / "cover_letter_example.pdf").resolve()

        generate_cover_letter(
            letter_path=str(letter_path),
            info_path=str(info_path),
            out_html=str(out_html),
            out_pdf=str(out_pdf),
        )

        assert out_html.exists()
        assert out_pdf.exists()

        # Validate HTML content
        html_content = out_html.read_text()
        assert len(html_content) > 100
        assert "<html" in html_content

        # Validate PDF structure
        validate_pdf_structure(out_pdf)

        # Clean up generated files
        out_html.unlink()
        out_pdf.unlink()

    def test_invalid_file_path_error(self, output_dir):
        """Test error handling for invalid file paths"""
        with pytest.raises(FileNotFoundError):
            generate_resume(resume_path="/nonexistent/file_example.json")

    def test_invalid_file_format_error(self, output_dir):
        """Test error handling for invalid file formats"""
        # Create a temporary file with invalid extension
        invalid_file = output_dir / "invalid.txt"
        invalid_file.write_text("some content")

        with pytest.raises((FileNotFoundError, ValueError, Exception)):
            generate_resume(resume_path=str(invalid_file))
