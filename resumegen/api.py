# Resume Generation API Server
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
import os
from pathlib import Path
import tempfile
import uuid
import base64

from resumegen.jinja_render import render_resume, render_cover_letter
from resumegen.models.resume import Resume
from resumegen.models.cover_letter import CoverLetter
from resumegen.models.personal_info import PersonalInfo
from resumegen.pdf_service import generate_pdf

app = FastAPI(
    title="Resume Generator API",
    description="Generate resumes and cover letters from JSON data",
    version="1.0.0",
)


# API Models
class ResumeRequest(BaseModel):
    resume_data: dict
    personal_info: dict
    output_format: str = "both"  # "html", "pdf", "both"


class CoverLetterRequest(BaseModel):
    cover_letter_data: dict
    personal_info: dict
    output_format: str = "both"  # "html", "pdf", "both"


class GenerationResponse(BaseModel):
    html_content: Optional[str] = None
    pdf_content: Optional[str] = None  # Base64 encoded PDF content
    message: str


# Temporary file storage (in production, use proper storage)
TEMP_DIR = Path("/tmp/resumegen")
TEMP_DIR.mkdir(exist_ok=True)


@app.get("/")
def root():
    return {"message": "Resume Generator API", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Resume Generator"}


@app.post("/generate-resume", response_model=GenerationResponse)
async def generate_resume_api(request: ResumeRequest):
    """Generate resume from JSON data"""
    try:
        # Parse and validate data
        personal_info = PersonalInfo(**request.personal_info)

        # Combine resume data with personal information
        resume_data_with_personal = {
            **request.resume_data,
            "personal_information": request.personal_info,
        }
        resume = Resume(**resume_data_with_personal)

        # Render HTML
        html_content = render_resume(resume)

        # Initialize response
        response = GenerationResponse(message="Resume generated successfully")

        # Generate outputs based on format
        if request.output_format in ["html", "both"]:
            response.html_content = html_content

        if request.output_format in ["pdf", "both"]:
            # Generate unique temporary files for PDF generation
            job_id = str(uuid.uuid4())[:8]
            html_file = TEMP_DIR / f"resume_{job_id}.html"
            pdf_file = TEMP_DIR / f"resume_{job_id}.pdf"

            # Save HTML temporarily
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_content)

            # Generate PDF
            generate_pdf(str(html_file), str(pdf_file))

            # Read PDF content and clean up temp files
            with open(pdf_file, "rb") as f:
                pdf_bytes = f.read()
                response.pdf_content = base64.b64encode(pdf_bytes).decode("utf-8")

            # Clean up temporary files
            html_file.unlink(missing_ok=True)
            pdf_file.unlink(missing_ok=True)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.post("/generate-cover-letter", response_model=GenerationResponse)
async def generate_cover_letter_api(request: CoverLetterRequest):
    """Generate cover letter from JSON data"""
    try:
        # Parse and validate data
        personal_info = PersonalInfo(**request.personal_info)

        # Combine cover letter data with personal information
        cover_letter_data_with_personal = {
            **request.cover_letter_data,
            "personal_information": request.personal_info,
        }
        cover_letter = CoverLetter(**cover_letter_data_with_personal)

        # Render HTML
        html_content = render_cover_letter(cover_letter)

        # Initialize response
        response = GenerationResponse(message="Cover letter generated successfully")

        # Generate outputs based on format
        if request.output_format in ["html", "both"]:
            response.html_content = html_content

        if request.output_format in ["pdf", "both"]:
            # Generate unique temporary files for PDF generation
            job_id = str(uuid.uuid4())[:8]
            html_file = TEMP_DIR / f"cover_letter_{job_id}.html"
            pdf_file = TEMP_DIR / f"cover_letter_{job_id}.pdf"

            # Save HTML temporarily
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_content)

            # Generate PDF
            generate_pdf(str(html_file), str(pdf_file))

            # Read PDF content and clean up temp files
            with open(pdf_file, "rb") as f:
                pdf_bytes = f.read()
                response.pdf_content = base64.b64encode(pdf_bytes).decode("utf-8")

            # Clean up temporary files
            html_file.unlink(missing_ok=True)
            pdf_file.unlink(missing_ok=True)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


# Run the server


@app.post("/generate-both")
async def generate_both(
    resume_data: dict, cover_letter_data: dict, personal_info: dict
):
    """Generate both resume and cover letter"""
    resume_request = ResumeRequest(
        resume_data=resume_data, personal_info=personal_info, output_format="both"
    )

    cover_letter_request = CoverLetterRequest(
        cover_letter_data=cover_letter_data,
        personal_info=personal_info,
        output_format="both",
    )

    resume_result = await generate_resume_api(resume_request)
    cover_letter_result = await generate_cover_letter_api(cover_letter_request)

    return {
        "resume": resume_result,
        "cover_letter": cover_letter_result,
        "message": "Both documents generated successfully",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
