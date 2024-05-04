from typing import List, Optional
# from pydantic import BaseModel, Field
from langchain_core.pydantic_v1 import BaseModel, Field


class PersonalDetails(BaseModel):
    name: str = Field(description="Name of the person")
    email: str = Field(description="Email id of the person")
    contact_num: str = Field(description="Phone Number of the person")

class Education(BaseModel):
    university: str = Field(description="Name of the university")
    degree: str = Field(description="Degree obtained")
    year_of_passing: Optional[int] = Field(description="Year of passing")
    field_of_study: Optional[str] = Field(description="Field of study")
    grade: Optional[str] = Field(description="Grade obtained")

class Project(BaseModel):
    project_name: str = Field(description="Title of the project")
    description: str = Field(description="Description of the project")

class Skill(BaseModel):
    skill_name: str = Field(description="Name of the skill")
    proficiency_level: str = Field(description="Proficiency level of the skill")

class WorkTask(BaseModel):
    task: str = Field(description="Task performed at the job")

class Experience(BaseModel):
    company_name: str = Field(description="Name of the company")
    job_role: str = Field(description="Job role at the company")
    duration: str = Field(description="Duration of the job")
    tasks: List[WorkTask] = Field(description="List of tasks performed at the job")

class Resume(BaseModel):
    personal_details: PersonalDetails
    education: List[Education]
    experience: List[Experience]
    skills: List[Skill]
    projects: List[Project]
    summary: str = Field(description="Brief summary of the candidate")