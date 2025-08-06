from typer import Typer, Option
from typing import Annotated
from pathlib import Path
import json
from resumegen.jinja_render import render_resume, render_cover_letter
from resumegen.storage import save_html, load_json
from resumegen.models import Resume, CoverLetter, PersonalInfo
from resumegen.pdf_service import generate_pdf
from rich import print

app = Typer(no_args_is_help=True)

DATA_PATH = Path(__file__).parent.parent / "data"


@app.command()
def generate_resume(
    resume_path: Annotated[
        str | None,
        Option(
            help="Path to the resume JSON file. Defaults to 'data/resume.json'.",
        ),
    ] = None,
    info_path: Annotated[
        str | None,
        Option(
            help="Path to the personal information JSON file. Defaults to 'data/personal_info.json'."
        ),
    ] = None,
    out_html: Annotated[
        str | None,
        Option(
            help="Path to save the generated HTML file. Defaults to 'data/resume.html'."
        ),
    ] = None,
    out_pdf: Annotated[
        str | None,
        Option(
            help="Path to save the generated PDF file. Defaults to 'data/resume.pdf'."
        ),
    ] = None,
) -> None:
    """
    Generate a resume in HTML and PDF format from a JSON input file.
    """

    if resume_path is None:
        resume_path = DATA_PATH / "resume.json"
    if info_path is None:
        info_path = DATA_PATH / "personal_info.json"
    if out_html is None:
        out_html = DATA_PATH / "resume.html"
    if out_pdf is None:
        out_pdf = DATA_PATH / "resume.pdf"

    info_path = Path(info_path).resolve()
    resume_path = Path(resume_path).resolve()
    out_html = Path(out_html).resolve()
    out_pdf = Path(out_pdf).resolve()

    resume_data = load_json(resume_path)
    info_data = load_json(info_path)

    resume = Resume(**resume_data, personal_information=info_data)

    html_content = render_resume(resume)
    save_html(html_content, out_html)
    print(f"Resume HTML saved to {out_html}")
    generate_pdf(out_html, out_pdf)
    print(f"Resume PDF saved to {out_pdf}")


@app.command()
def generate_cover_letter(
    letter_path: Annotated[
        str | None,
        Option(
            help="Path to the cover letter JSON file. Defaults to 'data/resume.json'."
        ),
    ] = None,
    info_path: Annotated[
        str | None,
        Option(
            help="Path to the personal information JSON file. Defaults to 'data/personal_info.json'."
        ),
    ] = None,
    out_html: Annotated[
        str | None,
        Option(
            help="Path to save the generated HTML file. Defaults to 'data/cover_letter.html'."
        ),
    ] = None,
    out_pdf: Annotated[
        str | None,
        Option(
            help="Path to save the generated PDF file. Defaults to 'data/cover_letter.pdf'."
        ),
    ] = None,
) -> None:
    """
    Generate a cover letter in HTML and PDF format from a JSON input file.
    """
    if info_path is None:
        info_path = DATA_PATH / "personal_info.json"
    if letter_path is None:
        letter_path = DATA_PATH / "cover_letter.json"
    if out_html is None:
        out_html = DATA_PATH / "cover_letter.html"
    if out_pdf is None:
        out_pdf = DATA_PATH / "cover_letter.pdf"

    info_path = Path(info_path).resolve()
    letter_path = Path(letter_path).resolve()
    out_html = Path(out_html).resolve()
    out_pdf = Path(out_pdf).resolve()

    info_data = load_json(info_path)
    letter_data = load_json(letter_path)

    cover_letter = CoverLetter(**letter_data, personal_information=info_data)

    html_content = render_cover_letter(cover_letter)
    save_html(html_content, out_html)
    print(f"Cover letter HTML saved to {out_html}")
    generate_pdf(out_html, out_pdf)
    print(f"Cover letter PDF saved to {out_pdf}")


if __name__ == "__main__":
    app()
