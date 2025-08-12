"""Utility functions for resume generation."""

from typing import Dict, Any, Optional
from resumegen.models.personal_info import PersonalInfo
from resumegen.models.resume import Resume
from resumegen.models.cover_letter import CoverLetter


def create_resume_with_personal_info(
    resume_data: Dict[str, Any], 
    personal_info_data: Optional[Dict[str, Any]] = None
) -> Resume:
    """
    Create a Resume object with proper personal information handling.
    
    Args:
        resume_data: Resume data dictionary
        personal_info_data: Optional personal information dictionary
        
    Returns:
        Resume object with personal information
        
    Raises:
        ValueError: If no personal information is available
    """
    # If personal info is provided directly, use it and remove from resume_data
    if personal_info_data is not None:
        # Validate the personal info
        PersonalInfo(**personal_info_data)
        
        # Remove personal_information from resume_data to avoid conflict
        resume_data_copy = resume_data.copy()
        if 'personal_information' in resume_data_copy:
            del resume_data_copy['personal_information']
        
        return Resume(**resume_data_copy, personal_information=personal_info_data)
    
    # If no personal info provided, check if it exists in resume data
    elif 'personal_information' in resume_data:
        # Validate the embedded personal info
        PersonalInfo(**resume_data['personal_information'])
        return Resume(**resume_data)
    
    # No personal information available anywhere
    else:
        raise ValueError(
            "Personal information not found. Please provide either personal_info_data "
            "parameter or include 'personal_information' in the resume_data."
        )


def create_cover_letter_with_personal_info(
    cover_letter_data: Dict[str, Any], 
    personal_info_data: Optional[Dict[str, Any]] = None
) -> CoverLetter:
    """
    Create a CoverLetter object with proper personal information handling.
    
    Args:
        cover_letter_data: Cover letter data dictionary
        personal_info_data: Optional personal information dictionary
        
    Returns:
        CoverLetter object with personal information
        
    Raises:
        ValueError: If no personal information is available
    """
    # If personal info is provided directly, use it and remove from cover_letter_data
    if personal_info_data is not None:
        # Validate the personal info
        PersonalInfo(**personal_info_data)
        
        # Remove personal_information from cover_letter_data to avoid conflict
        cover_letter_data_copy = cover_letter_data.copy()
        if 'personal_information' in cover_letter_data_copy:
            del cover_letter_data_copy['personal_information']
        
        return CoverLetter(**cover_letter_data_copy, personal_information=personal_info_data)
    
    # If no personal info provided, check if it exists in cover letter data
    elif 'personal_information' in cover_letter_data:
        # Validate the embedded personal info
        PersonalInfo(**cover_letter_data['personal_information'])
        return CoverLetter(**cover_letter_data)
    
    # No personal information available anywhere
    else:
        raise ValueError(
            "Personal information not found. Please provide either personal_info_data "
            "parameter or include 'personal_information' in the cover_letter_data."
        )