import os
import google.generativeai as genai
import streamlit as st
from pdf_text_extractor import extract_text
from dotenv import load_dotenv

load_dotenv() # Activate API Key

# Configure Model

api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-flash-lite-latest')

st.header('SKILL_MATCHER :blue[AI assisted skill matching tool]', divider ='green')

st.subheader('Tips to use the tool')

tips = '''* Upload your resume in slide bar (PDF only).
* Copy and paste Job decription for job you are applying for.
* Submit'''

st.write(tips)

st.sidebar.header('Upload your PDF here', divider = 'green')
st.sidebar.subheader('Upload PDF file only')
pdf_doc = st.sidebar.file_uploader('Resume', type=['pdf'])

pdf_text = None

if pdf_doc:
    pdf_text = extract_text(pdf_doc)
else:
    st.sidebar.write('Upload the PDF first')

job_desc = st.text_area('copy and paste your job description (press ctrl+enter to submit)', max_chars=10000)

prompt = f'''Assuming you are an expert in job skill matching and profile short listing.
You have the resume = {pdf_text} and job description = {job_desc}. Using this data generate the
output on the following outline
* Calculate and show the ATS score. Discuss matching and non matching keywords (max 2 line discussion).
* Claculate and show the chances of selection of profile (One line discussion)
* Perform SWOT analysis and discuss in bullet points.
* Discuss in bullet points what the positives in the resume that will help in getting shortlisted.
* Discuss in bullet points what other things can be mentioned and discussed in resume.
* Prepare two revised resume's for this particular job description with chances of selection 
being maximised while implementing all the points discussed above.
* Prepare these resume in such a way that it can be copied and pasted in word and generate pdf.'''

if job_desc:
    if pdf_doc == None:
        st.write('You forget to upload resume')
    else:
        with st.spinner('Processing your resume and Job description...'):
            response = model.generate_content(prompt)

        st.success('Processing Completed')
        st.write(response.text )