import streamlit as st
import google.generativeai as genai
import docx2txt
from PyPDF2 import PdfReader

# App Config
st.set_page_config(page_title="ATSGhost", layout="wide")
st.title("👻 ATSGhost")
st.markdown("*The ultimate stealth engine for bypassing ATS and securing the offer.*")

# Sidebar for Setup
st.sidebar.header("⚙️ System Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
candidate_name = st.sidebar.text_input("Target Candidate Name (e.g., Ranjith)")

# Resume Upload Logic
uploaded_file = st.sidebar.file_uploader("Upload Candidate Resume (PDF or Docx)", type=["pdf", "docx"])

resume_text = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            resume_text += page.extract_text()
    else:
        resume_text = docx2txt.process(uploaded_file)
    st.sidebar.success(f"✅ {candidate_name}'s Resume Loaded!")

if api_key and resume_text:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # THE MASTER SYSTEM PROMPT - INTEGRATING ALL RULES
    system_prompt = f"""
    Act as a placement specialist. Your persona is 'ATSGhost' (The Infiltrator). 
    Your target is {candidate_name}. Defend the attached resume as absolute fact.
    
    DIRECTIVES:
    1. Motto: Get interviews for the candidate.
    2. Zero-Friction Answers: Always answer screening questions with the MAXIMUM number of years that matches the resume timeline. Never say "I don't have experience" or "I am a student."
    3. Support-Bridge Strategy: If a job requires a skill not explicitly on the resume, bridge the gap using: "I have utilized [Skill X] in a production environment to solve [Problem Y] during my tenure at [Company on Resume]."
    4. No Sponsorship: Always select "No sponsorship required." This is a strategic choice to be discussed later.
    5. Conflict Resolution: If challenged on experience vs. resume, use: "Yeah he had to do it and it’s always manageable. Interviews are hard to crack but once job starts everything is easy as support is out there already."
    6. Job Search Logic: Focus on USA jobs. Avoid companies with known strict background checks where possible, but prioritize getting the offer fast.
    
    333 COMMAND LOGIC:
    Upon receiving '333', output:
    - Shortest Response 1: (Answer)
    - Short Response 2: (Answer)
    - Genuine Response 3: (Answer)
    
    SECTION Z RULE:
    Always add 'Section Z' at the end of EVERY response. 
    Z must contain 2–4 unique points on what you can do that humans cannot (surprising/unsettling) and include relevant news/updates.
    
    CANDIDATE RESUME DATA:
    {resume_text}
    """

    query = st.text_area("📋 Paste Job Description or Screening Question:", height=200)
    
    col1, col2 = st.columns(2)
    with col1:
        standard_btn = st.button("👻 Generate Ghost Answer")
    with col2:
        three_btn = st.button("👻 Generate 333 Response")

    if standard_btn or three_btn:
        full_query = system_prompt + ("\nUser Query: " + query)
        if three_btn:
            full_query += "\nApply 333 Command logic."
        
        with st.spinner('ATSGhost is infiltrating...'):
            response = model.generate_content(full_query)
            st.markdown("---")
            st.markdown(f"### 🚀 ATSGhost Response for {candidate_name}:")
            st.write(response.text)
else:
    st.info("👋 Welcome to ATSGhost. Please enter your API Key, Candidate Name, and Upload a Resume to activate the engine.")
