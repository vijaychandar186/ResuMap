import json

RESUME_TEMPLATE: dict = {
    "name": "",
    "email": "",
    "phone": "",
    "location": "",
    "skills": [],
    "experience": [
        {
            "company": "",
            "title": "",
            "start_date": "",
            "end_date": "",
            "location": "",
        }
    ],
    "education": [
        {
            "degree": "",
            "institution": "",
            "year": "",
        }
    ],
}


def get_template_str() -> str:
    """Pretty-printed JSON string as required by NuExtract prompt format."""
    return json.dumps(RESUME_TEMPLATE, indent=4)
