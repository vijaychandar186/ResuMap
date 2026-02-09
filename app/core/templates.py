import json

RESUME_TEMPLATE: dict = {
    "personal_information": {
        "name": "",
        "email": "",
        "phone": "",
        "location": "",
    },
    "skills": [],
    "work_experience": [
        {
            "employer": "",
            "job_title": "",
            "start_date": "",
            "end_date": "",
            "location": "",
        }
    ],
    "education": [
        {
            "degree": "",
            "institution": "",
            "graduation_year": "",
        }
    ],
}


def get_template_str() -> str:
    """Pretty-printed JSON string as required by NuExtract prompt format."""
    return json.dumps(RESUME_TEMPLATE, indent=4)