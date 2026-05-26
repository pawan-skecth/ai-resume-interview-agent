import streamlit as st

from utils.resume_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.role_requirements import get_role_requirements
from utils.embedding_matcher import embedding_skill_matching
from utils.llm_engine import ask_llm
from utils.interview_generator import generate_interview_questions


st.set_page_config(
    page_title="AI Resume Interview Agent",
    layout="wide"
)

st.title("🤖 AI Resume Screening & Interview Agent")

st.write("Upload your resume for AI analysis")


# =========================================================
# SESSION STATE
# =========================================================
if "feedback" not in st.session_state:
    st.session_state.feedback = None

if "questions" not in st.session_state:
    st.session_state.questions = None


# =========================================================
# RESUME UPLOAD
# =========================================================
uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"],
    key="resume_uploader"
)


# =========================================================
# ATS MATCHING SECTION
# =========================================================
st.header("🎯 ATS Matching")

role = st.text_input(
    "Enter Target Role (Optional)",
    placeholder="Example: Data Scientist"
)

jd_text = st.text_area(
    "Paste Job Description (Optional)",
    height=200,
    placeholder="Paste Job Description here..."
)


# =========================================================
# INTERVIEW SECTION
# =========================================================
st.header("🎤 AI Interview Question Generator")

interview_role = st.text_input(
    "Enter Job Role",
    placeholder="Example: Data Scientist"
)

interview_topics = st.text_input(
    "Enter Topics (Comma Separated)",
    placeholder="Example: Python, SQL, Machine Learning"
)

technical_question_count = st.number_input(
    "Technical Questions Per Topic",
    min_value=1,
    max_value=100,
    value=10
)

difficulty_level = st.selectbox(
    "Difficulty Level",
    ["Easy", "Medium", "Hard"]
)


# =========================================================
# MAIN FLOW
# =========================================================
if uploaded_file is not None:

    resume_text = extract_text_from_pdf(uploaded_file)

    st.success("Resume uploaded successfully!")

    st.subheader("Extracted Resume")

    st.text_area(
        "Resume Content",
        resume_text,
        height=250
    )

    # =====================================================
    # RESUME SKILLS
    # =====================================================
    detected_skills = extract_skills(resume_text)

    st.subheader("Detected Resume Skills")
    st.write(detected_skills)

    required_skills = []
    score = 0
    matched = []
    missing = []

    # =====================================================
    # JD BASED MATCHING (PRIORITY)
    # =====================================================
    if jd_text.strip() != "":

        st.info("Using Job Description Based Matching")

        required_skills = extract_skills(jd_text)

        st.subheader("JD Skills")
        st.write(required_skills)

        with st.spinner("Performing semantic skill matching..."):

            score, matched, missing = embedding_skill_matching(
                detected_skills,
                required_skills
            )

        st.subheader("ATS Score")
        st.metric("Match Score", f"{score}%")

        st.subheader("Matched Skills")
        st.write(matched)

        st.subheader("Missing Skills")
        st.write(missing)

    # =====================================================
    # ROLE BASED MATCHING
    # =====================================================
    elif role.strip() != "":

        st.info("Using Role Based Matching")

        with st.spinner("Generating required skills..."):

            required_skills = get_role_requirements(role)

        st.subheader("Required Skills")
        st.write(required_skills)

        with st.spinner("Performing semantic skill matching..."):

            score, matched, missing = embedding_skill_matching(
                detected_skills,
                required_skills
            )

        st.subheader("ATS Score")
        st.metric("Match Score", f"{score}%")

        st.subheader("Matched Skills")
        st.write(matched)

        st.subheader("Missing Skills")
        st.write(missing)

    # =====================================================
    # AI FEEDBACK
    # =====================================================
    if required_skills:

        st.subheader("AI Resume Feedback")

        use_feedback_role = st.checkbox(
            "Use Job Role For Better Suggestions"
        )

        feedback_role = ""

        if use_feedback_role:

            feedback_role = st.text_input(
                "Enter Job Role For Feedback",
                placeholder="Example: Generative AI Engineer"
            )

        if st.button("Generate AI Feedback"):

            prompt = f"""
You are an expert ATS resume reviewer and career mentor.

IMPORTANT RULES:

1. ATS evaluation should mainly depend on:
- matched skills
- missing skills
- resume quality
- technical gaps

2. If a target role is provided,
use it ONLY for:
- improvement suggestions
- career guidance
- missing technologies
- industry expectations

3. Do NOT completely depend on role.
Mainly evaluate using resume skills and matching.

--------------------------------------------------

TARGET ROLE:
{feedback_role}

--------------------------------------------------

RESUME:
{resume_text}

--------------------------------------------------

RESUME SKILLS:
{detected_skills}

--------------------------------------------------

REQUIRED SKILLS:
{required_skills}

--------------------------------------------------

ATS MATCH SCORE:
{score}

--------------------------------------------------

MATCHED SKILLS:
{matched}

--------------------------------------------------

MISSING SKILLS:
{missing}

--------------------------------------------------

Provide detailed:

1. Resume Strengths

2. Resume Weaknesses

3. Important Missing Skills

4. Technical Improvement Suggestions

5. Career Guidance

6. Resume Enhancement Suggestions

7. Hiring Probability

If a target role is provided,
mention role-specific missing technologies
and improvements.
"""

            with st.spinner("Generating feedback..."):

                st.session_state.feedback = ask_llm(prompt)

        if st.session_state.feedback:

            st.write(st.session_state.feedback)

    # =====================================================
    # INTERVIEW QUESTIONS
    # =====================================================
    if interview_role.strip() != "":

        st.subheader("AI Interview Questions")

        if st.button("Generate Interview Questions"):

            with st.spinner("Generating interview questions..."):

                st.session_state.questions = generate_interview_questions(
                    interview_role,
                    interview_topics,
                    technical_question_count,
                    difficulty_level
                )

        if st.session_state.questions:

            st.write(st.session_state.questions)