import streamlit as st
import openai
import PyPDF2
import docx

# OpenAI API Key (Replace with your actual API key)
OPENAI_API_KEY = "give your API key here"
client = openai.OpenAI(api_key=OPENAI_API_KEY)  # ✅ Updated API format

# Function to extract text from a PDF file
def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Function to analyze resume and provide feedback
def get_resume_feedback(resume_text):
    prompt = f"""
    Please analyze the following resume and provide improvement suggestions.
    Identify missing skills, suggest better wording, and recommend additional experiences or projects.

    Resume Content:
    {resume_text}
    """

    response = client.chat.completions.create(  # ✅ New OpenAI API format
        model="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" if you prefer a cheaper option
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# Streamlit UI
st.title("AI Resume Analyzer & Career Guidance")

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]

    # Extract resume text
    if file_extension == "pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    elif file_extension == "docx":
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file format.")
        resume_text = ""

    if resume_text:
        # Display Extracted Resume Content
        st.subheader("Extracted Resume Content")
        st.text(resume_text[:1000])  # Show only first 1000 characters for readability

        # Get AI-based feedback
        st.subheader("AI Resume Feedback")
        with st.spinner("Analyzing your resume..."):
            feedback = get_resume_feedback(resume_text)
        
        st.write(feedback)