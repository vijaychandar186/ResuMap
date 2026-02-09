from pydantic import BaseModel, Field


class ExperienceItem(BaseModel):
    employer: str = ""
    job_title: str = ""
    start_date: str = ""
    end_date: str = ""
    location: str = ""


class EducationItem(BaseModel):
    degree: str = ""
    institution: str = ""
    graduation_year: str = ""


class PersonalInformation(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""


class ResumeExtraction(BaseModel):
    personal_information: PersonalInformation = Field(default_factory=PersonalInformation)
    skills: list[str] = Field(default_factory=list)
    work_experience: list[ExperienceItem] = Field(default_factory=list)
    education: list[EducationItem] = Field(default_factory=list)


class ExtractionResponse(BaseModel):
    success: bool
    data: ResumeExtraction | None = None
    error: str | None = None
    chunks_processed: int = 1
