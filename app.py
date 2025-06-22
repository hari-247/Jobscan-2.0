import streamlit as st
from config import OLLAMA_MODEL, OLLAMA_API_URL
from ollama_client import get_ollama_response
from file_utils import extract_text_from_pdf, create_docx_from_json
from prompts import get_analysis_prompt, get_generation_prompt


st.set_page_config(page_title="AI Resume Enhancer", page_icon="⚽️", layout="wide")
st.title(" AI Resume Enhancer")
st.markdown("Analyze your resume against a job description, identify gaps, and generate an improved version.")


if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'generated_docx' not in st.session_state:
    st.session_state.generated_docx = None


st.header("Step 1: Provide Your Resume and Job Description")
col1, col2 = st.columns(2)

with col1:
    uploaded_resume = st.file_uploader("Upload Your Resume (PDF)", type="pdf")
    if uploaded_resume:
        text, error = extract_text_from_pdf(uploaded_resume)
        if error:
            st.error(error)
        else:
            st.session_state.resume_text = text
            with st.expander("View Extracted Resume Text"):
                st.text_area("", st.session_state.resume_text, height=200)

with col2:
    st.session_state.job_description = st.text_area(
        "Paste the Job Description Here", st.session_state.job_description, height=300)

if st.button("Analyze Resume", type="primary", use_container_width=True):
    if not st.session_state.resume_text or not st.session_state.job_description:
        st.error("Please upload a resume and paste a job description.")
    else:
        with st.spinner(f"Analyzing with {OLLAMA_MODEL}... This may take a moment."):
            analysis_prompt = get_analysis_prompt(st.session_state.job_description, st.session_state.resume_text)
            result, error = get_ollama_response(analysis_prompt)
            if error:
                st.error(error)
                st.session_state.analysis_result = None
            else:
                st.session_state.analysis_result = result
                st.success("Analysis complete!")


if st.session_state.analysis_result:
    st.header("Step 2: Review Your Analysis")
    res = st.session_state.analysis_result
    
    score_col1, score_col2 = st.columns(2)
    score_col1.metric("Overall Match Score", f"{res.get('overall_score', 0)} / 100")
    score_col1.progress(res.get('overall_score', 0) / 100)
    score_col2.metric("ATS Friendliness Score", f"{res.get('ats_friendliness_score', 0)} / 100")
    score_col2.progress(res.get('ats_friendliness_score', 0) / 100)

    st.info(f"**Summary & Suggestions:** {res.get('summary_and_suggestions', 'N/A')}")

    with st.expander("Keyword & Skill Gap Analysis"):
        kw_col1, kw_col2 = st.columns(2)
        kw_col1.success("Matching Keywords")
        kw_col1.multiselect("Keywords Found", options=res.get('matching_keywords', []), default=res.get('matching_keywords', []))
        kw_col2.warning("Missing Keywords")
        kw_col2.multiselect("Keywords to Add", options=res.get('missing_keywords', []), default=res.get('missing_keywords', []))
        st.write("**Skill Gap Deep Dive:**", res.get('skill_gap_analysis', 'N/A'))
            
    with st.expander("ATS Friendliness Feedback"):
        st.write(res.get('ats_friendliness_feedback', 'N/A'))

    
    st.header("Step 3: Generate an Improved Resume")
    st.markdown("Upload a resume template (PDF) to guide the AI's structure.")
    uploaded_template = st.file_uploader("Upload Resume Template (PDF)", type="pdf", key="template_uploader")
    
    if uploaded_template:
        template_text, error = extract_text_from_pdf(uploaded_template)
        if error:
            st.error(error)
        elif st.button("Generate New Resume", type="primary", use_container_width=True):
            with st.spinner(f"Re-drafting your resume with {OLLAMA_MODEL}..."):
                gen_prompt = get_generation_prompt(st.session_state.resume_text, st.session_state.job_description, res, template_text)
                new_resume_json, error = get_ollama_response(gen_prompt)

                if error:
                    st.error(error)
                else:
                    st.success("New resume generated!")
                    st.session_state.generated_docx = create_docx_from_json(new_resume_json)
                    with st.expander("Preview Generated Resume Data (JSON)", expanded=True):
                        st.json(new_resume_json)

if st.session_state.get('generated_docx'):
    st.download_button(
        label="📥 Download Resume as DOCX",
        data=st.session_state.generated_docx,
        file_name="Enhanced_Resume.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    )

# --- Sidebar ---
with st.sidebar:
    st.header("How it Works")
    st.info(
        "1. **Upload & Paste:** Add your resume PDF and the job description.\n"
        "2. **Analyze:** The AI scores your resume and finds gaps.\n"
        "3. **Upload Template:** Provide a PDF of a resume with a format you like.\n"
        "4. **Generate & Download:** The AI rewrites your resume content into the new structure, ready to download as a DOCX file."
    )
    st.warning(f"**Model:** `{OLLAMA_MODEL}`\n**API:** `{OLLAMA_API_URL}`\n\nEnsure your local Ollama server is running.")