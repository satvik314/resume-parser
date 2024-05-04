import streamlit as st
from utils import extract_info, read_pdf, resume_to_dataframe
from models import Resume
from langchain_openai import ChatOpenAI

# Defining LLM
# llm = ChatOpenAI(model = "gpt-3.5-turbo")

llama3_groq = ChatOpenAI(
    model = "llama3-70b-8192",
    openai_api_base = "https://api.groq.com/openai/v1",
    openai_api_key = st.secrets["GROQ_API_KEY"]
)




def main():
    st.title("XScaleUp Resume")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Read PDF file
        resume_text = read_pdf(uploaded_file)
        print(resume_text)
        
        # Extract information from resume
        resume_info = extract_info(resume_text, llama3_groq)

        df = resume_to_dataframe(resume_info)

        # Convert DataFrame to CSV
        csv = df.to_csv(index=False).encode('utf-8')

        # Create a download button for the CSV file
        st.download_button(
            label="Download Resume Data as CSV",
            data=csv,
            file_name="resume_data.csv",
            mime="text/csv",
        )
        
        # Display extracted information
        st.subheader("View resume data")
        st.json(resume_info.dict())

        # Convert DataFrame to CSV
        csv = df.to_csv(index=False).encode('utf-8')

        # Create a download button for the CSV file
        st.download_button(
            label="Download Resume Data as CSV",
            data=csv,
            file_name="resume_data.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()



