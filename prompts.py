
def get_analysis_prompt(job_description: str, resume_text: str) -> str:

    return f"""
    As an expert HR analyst and resume reviewer, your task is to analyze the following resume against the provided job description.
    Provide a detailed analysis in a pure JSON format. The JSON object must contain the following keys:
    - "overall_score": An integer score from 0 to 100 representing how well the resume matches the job description.
    - "ats_friendliness_score": An integer score from 0 to 100 on how well the resume is structured for Applicant Tracking Systems (ATS). Consider factors like standard sections, clear headings, and parsable format.
    - "ats_friendliness_feedback": A string with concrete suggestions on how to improve ATS compatibility.
    - "matching_keywords": A list of important keywords and skills from the job description that ARE present in the resume, ensure that these keywords relate to the job descrption and not to some random content abou the company that is not realvant to the resume 
    - "missing_keywords": A list of important keywords and skills from the job description that ARE MISSING from the resume.
    - "skill_gap_analysis": A string that elaborates on the missing skills and experiences make them clear, explaining their importance for the role.
    - "summary_and_suggestions": A brief string summarizing the resume's strengths and weaknesses and providing overall suggestions for improvement.

    Do not include any text, explanations, or markdown formatting outside of the JSON object itself.

    JOB DESCRIPTION:
    ---
    {job_description}
    ---

    RESUME TEXT:
    ---
    {resume_text}
    ---
    """

def get_generation_prompt(resume_text: str, job_description: str, analysis_result: dict, template_text: str) -> str:
    return f"""
    You are an expert resume writer. Your task is to create a new, enhanced resume by rewriting the user's original resume.
    You will be given the user's original resume, a job description, an analysis of skill gaps, and a resume template for structure.
    Your goal is to rewrite the resume to:
    1.  Incorporate the "missing keywords" and address the "skill gap analysis".
    2.  Tailor the experience and summary to the specific job description.
    3.  Maintain the user's original experience, but rephrase it professionally using action verbs and quantifiable results.
    4.  Structure the output to follow the provided template's sections.
    5.  Return ONLY a valid JSON object. Do not add any introductory text, explanations, or markdown formatting.

    The JSON output must be strictly structured as follows:
    {{
      "contact": {{ "name": "...", "email": "...", "phone": "...", "linkedin": "..." }},
      "summary": "A 2-3 sentence professional summary tailored to the job.",
      "experience": [
        {{ "title": "...", "company": "...", "location": "...", "dates": "...", "description": ["bullet point 1", "bullet point 2"] }}
      ],
      "education": [
        {{ "institution": "...", "degree": "...", "location": "...", "dates": "..." }}
      ],
      "skills": ["Skill 1", "Skill 2", "Relevant Technology"],
      "projects": [
         {{ "title": "...", "description": "..." }}
      ]
    }}

    If a section (like 'projects') is not present in the original resume or template, you may omit it from the JSON.

    ---
    ORIGINAL RESUME TEXT:
    {resume_text}
    ---
    JOB DESCRIPTION:
    {job_description}
    ---
    ANALYSIS (Gaps to fill):
    Missing Keywords: {analysis_result.get('missing_keywords', [])}
    Skill Gap Analysis: {analysis_result.get('skill_gap_analysis', '')}
    ---
    RESUME TEMPLATE (for structure and section headers):
    {template_text}
    ---
    """