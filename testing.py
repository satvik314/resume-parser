import streamlit as st
from utils import extract_info, read_pdf, resume_to_dataframe
from models import Resume
from langchain_openai import ChatOpenAI
import pandas as pd

# Defining LLM
openai_api_key = st.secrets["OPENAI_API_KEY"]
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Cache the LLM responses
@st.cache_resource
def get_llm():
    return llm

# Cache the extracted resume information
@st.cache_data
def cache_resume_info(resume_text):
    llm = get_llm()
    return extract_info(resume_text, llm)

def main():
    st.title("XScaleUp Resume")
    st.subheader("Convert resume -> CSV")

    # File uploader
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        if len(uploaded_files) > 10:
            st.error("You can upload a maximum of 10 files at a time.")
        else:
            all_resume_info = []
            all_dfs = []
            for uploaded_file in uploaded_files:
                resume_text = read_pdf(uploaded_file)
                if resume_text:
                    # Retrieve cached resume information or extract new information
                    resume_info = cache_resume_info(resume_text)
                    if resume_info:
                        all_resume_info.append(resume_info)
                        df = resume_to_dataframe(resume_info)
                        if not df.empty:
                            all_dfs.append(df)

                    # Display extracted information
                    st.subheader(f"View resume data for {uploaded_file.name}")
                    st.json(resume_info.dict())

            if all_dfs:
                # Combine all dataframes into one
                combined_df = pd.concat(all_dfs, ignore_index=True)

                # Convert DataFrame to CSV
                csv = combined_df.to_csv(index=False).encode('utf-8')

                # Create a download button for the CSV file
                st.download_button(
                    label="Download Combined Resume Data as CSV",
                    data=csv,
                    file_name="combined_resume_data.csv",
                    mime="text/csv",
                )

if __name__ == "__main__":
    main()