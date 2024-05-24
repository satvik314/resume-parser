import re
import PyPDF2
import base64
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from models import Resume
import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI



# # Defining LLM
# llama3_groq = ChatOpenAI(
#     model = "llama3-70b-8192",
#     openai_api_base = "https://api.groq.com/openai/v1",
#     openai_api_key = st.secrets["GROQ_API_KEY"]
# )

llm = ChatOpenAI(model = "gpt-3.5-turbo")


def read_pdf(file):
    """
    Reads a resume in PDF file and extract text from it.
    :param file: File object
    :return: String
    """
    reader = PyPDF2.PdfReader(file)
    num_pages = len(reader.pages)
    text = ""
    for i in range(num_pages):
        page = reader.pages[i]
        text += page.extract_text()
    return text


def extract_info(resume: str, model = llm):
    """
    Extracts sections from the resume
    :param resume:
    :return:
    """
    llm = model 
    # parser = OutputFixingParser.from_llm(parser=PydanticOutputParser(pydantic_object=Resume), llm=llm)
    # Correct instantiation of PydanticOutputParser with the Resume class
    parser = OutputFixingParser.from_llm(parser=PydanticOutputParser(pydantic_object=Resume), llm=llm)
    format_instructions = parser.get_format_instructions()
    resume_text = llm.predict(
        f"Given a resume {resume} \n Extract all the relevant sections.  \n {format_instructions}")
    resume_info = parser.parse(resume_text)
    return resume_info

def resume_to_dataframe(resume: Resume) -> pd.DataFrame:
    data = {
        "name": resume.personal_details.name,
        "email": resume.personal_details.email,
        "contact_num": resume.personal_details.contact_num,
        "university": resume.education[0].university if resume.education else None,
        "latest_company_name": resume.experience[0].company_name if resume.experience else None,
        "latest_job_role": resume.experience[0].job_role if resume.experience else None,
        "summary": resume.summary
    }
    return pd.DataFrame([data])
