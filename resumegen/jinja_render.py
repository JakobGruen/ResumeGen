# filepath: src/jinja_resume.py
from jinja2 import Environment, FileSystemLoader, select_autoescape
from resumegen.models import Resume, CoverLetter, PersonalInfo
from pathlib import Path
import os
from datetime import datetime

TEMPLATE_DIR = Path(__file__).parent / "templates"
STYLE_NAME = "style.css"
RESUME_TEMPLATE_NAME = "resume_template.html.j2"
COVER_LETTER_TEMPLATE_NAME = "cover_letter_template.html.j2"


def render_resume(
    resume: Resume,
    wd: Path = TEMPLATE_DIR,
    style_name: str = STYLE_NAME,
    template_name: str = RESUME_TEMPLATE_NAME,
) -> str:
    """
    Render a Resume object to HTML using Jinja2 template.
    """
    env = Environment(
        loader=FileSystemLoader(wd), autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template(template_name)
    with open(wd / style_name, "r", encoding="utf-8") as f:
        style_css = f.read()
    # Defensive: ensure all sections are at least empty lists for template logic
    resume_dict = resume.model_dump()
    for section in [
        "education",
        "work_experience",
        "projects",
        "achievements",
        "certifications",
        "additional_skills",
    ]:
        if resume_dict.get(section) is None:
            resume_dict[section] = []
    html = template.render(**resume_dict, style_css=style_css)
    return html


def render_cover_letter(
    cover_letter: CoverLetter,
    date=None,
    wd: Path = TEMPLATE_DIR,
    template_name: str = COVER_LETTER_TEMPLATE_NAME,
    style_name: str = STYLE_NAME,
) -> str:
    """
    Render a CoverLetter object to HTML using Jinja2 template and Resume for personal info.
    """
    if date is None:
        date = datetime.now().strftime("%d-%m-%Y")

    env = Environment(
        loader=FileSystemLoader(wd), autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template(template_name)
    with open(wd / style_name, "r", encoding="utf-8") as f:
        style_css = f.read()
    # Defensive: ensure personal_information exists
    cover_letter_dict = cover_letter.model_dump()
    if cover_letter_dict.get("personal_information") is None:
        cover_letter_dict["personal_information"] = {}
    html = template.render(
        **cover_letter_dict,
        date=date,
        style_css=style_css,
    )
    return html
