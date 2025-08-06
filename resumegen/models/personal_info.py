# resumegen/models/personal_info.py
from pydantic import BaseModel, Field


class PersonalInfo(BaseModel):
    """
    Personal information of the candidate.
    """

    name: str = Field(..., description="First name of the candidate.")
    surname: str = Field(..., description="Surname of the candidate.")
    date_of_birth: str = Field(
        ..., description="Date of birth of the candidate in DD/MM/YYYY format."
    )
    address: str = Field(..., description="Street Address of the candidate.")
    city: str = Field(..., description="City of residence of the candidate.")
    country: str = Field(..., description="Country of residence of the candidate.")
    zip_code: str = Field(..., description="Zip code of the candidate's address.")
    email: str = Field(..., description="email address of the candidate.")
    phone: str = Field(..., description="Phone number of the candidate (with prefix).")
    linkedin: str | None = Field(
        None, description="LinkedIn profile URL of the candidate."
    )
    github: str | None = Field(None, description="GitHub profile URL of the candidate.")
