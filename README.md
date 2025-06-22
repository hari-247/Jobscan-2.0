# AI Resume Enhancer & ATS Analyzer

A powerful **Streamlit** application that leverages a local Large Language Model (LLM) via **Ollama** to analyze your resume against a job description. It provides a detailed analysis, including an ATS-friendliness score and keyword matching, and then helps you generate an improved, tailored version of your resume that you can download as a `.docx` file.

![Demo Image -1](images/demo-1.png)

![Demo Image -2](images/demo-2.png)

## Key Features

- **PDF Resume Parsing:** Easily upload your resume in PDF format, and the application will extract the text for analysis.
- **Detailed Job Analysis:** Paste any job description to serve as the benchmark for the resume review.
- **Comprehensive AI Analysis:** Get a multi-faceted review of your resume, including:
  - **Overall Match Score:** A percentage score indicating how well your resume aligns with the job description.
  - **ATS Friendliness Score:** A rating of how well your resume is structured for Applicant Tracking Systems, complete with actionable feedback.
  - **Keyword Analysis:** See which crucial keywords from the job description are present in your resume and, more importantly, which ones are missing.
  - **Skill Gap Summary:** A qualitative analysis of the skills and experiences you should highlight or add.
- **Template-Based Regeneration:** Upload a PDF of a resume whose style and structure you admire. The AI will use it as a template for your new resume.
- **AI-Powered Content Rewriting:** The application intelligently rewrites your professional summary and experience bullet points to incorporate missing keywords and align with the job's requirements, using strong action verbs.
- **Download as DOCX:** Download the newly generated, enhanced resume as a fully editable Microsoft Word (`.docx`) file.
- **Modular & Clean Codebase:** The project is logically split into modules for configuration, API communication, utility functions, and UI, making it easy to understand and extend.

---

## 📁 Project Structure

```
resume_enhancer_project/
├── app.py              # Main Streamlit application file (UI and orchestration)
├── config.py           # Stores configuration constants (model name, API URL)
├── ollama_client.py    # Handles all communication with the Ollama API
├── file_utils.py       # Helper functions for PDF reading and DOCX creation
├── prompts.py          # Contains the large, structured prompts for the AI
├── README.md           # This documentation file
└── requirements.txt    # Lists all necessary Python packages
```

---

## Setup and Installation

### 1. Prerequisites: Install Ollama

This application requires a running Ollama instance to serve the local LLM.

- Download and install Ollama from the [official website](https://ollama.com/).
- Once Ollama is installed and running, pull the model specified in the configuration. As of June 2025, `llama3.2:3b` is a powerful and efficient model for this task.

```bash
ollama pull llama3.2:3b
```

> **Ensure the Ollama application is running in the background before starting the Streamlit app.**

---

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd resume_enhancer_project
```

---

### 3. Create a Virtual Environment (Recommended)

It's a best practice to create a virtual environment to manage project-specific dependencies.

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

---

### 4. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

---

## How to Run the Application

1. **Ensure Ollama is running.**
2. **Navigate to the project directory in your terminal.**
3. **Launch the Streamlit application:**

```bash
streamlit run app.py
```

Your web browser should open a new tab with the "AI Resume Enhancer" application.

---

## How to Use the App

The application flow is divided into three simple steps on the UI:

### **Step 1: Provide Inputs**

- Upload your current resume as a PDF file.
- Paste the complete job description into the corresponding text area.
- Click the **"Analyze Resume"** button.

### **Step 2: Review Analysis**

- Examine your Overall Match and ATS Friendliness scores.
- Read the AI's summary and suggestions.
- Expand the detailed sections to see which keywords are missing and to understand the skill gap analysis.

### **Step 3: Generate & Download New Resume**

- Upload a PDF of a resume whose formatting you like to act as a structural template.
- Click the **"Generate New Resume"** button. The AI will use your original content, the job requirements, and the template's structure to create an improved version.
- After a moment, a JSON preview of the new resume will appear.
- Click the **"Download Resume as DOCX"** button to save the final document.

---

## Configuration

You can easily change the Ollama model or API URL by editing the `config.py` file.

```python
# config.py

# The full URL to your local Ollama API endpoint.
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# The model to use. Make sure you have pulled it via 'ollama pull <model_name>'
OLLAMA_MODEL = "llama3.2:3b"
```
