import streamlit as st
from resume_parser import parse_pdf
from ats_engine import calculate_ats_score
from ai_enhancer import enhance_resume, feedback_chat

st.set_page_config(page_title="AI Resume ATS Optimizer", layout="wide")

st.title("📄 AI-Powered Resume Builder & ATS Optimization Agent")

# ---------------- INPUT SECTION ----------------
st.header("1️⃣ Upload Resume & Job Description")

uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])
job_description = st.text_area("Paste Job Description", height=200)

resume_text = ""

if uploaded_file:
    resume_text = parse_pdf(uploaded_file)
    st.success("Resume uploaded and parsed successfully")

# ---------------- ATS SCORE BEFORE ----------------
if resume_text and job_description:
    st.header("2️⃣ ATS Score (Before Enhancement)")

    score_before, missing_keywords = calculate_ats_score(resume_text, job_description)

    st.metric("ATS Score (Before)", f"{score_before}/100")
    st.progress(score_before / 100)

    if missing_keywords:
        st.warning("Missing Keywords:")
        st.write(", ".join(missing_keywords))

# ---------------- AI ENHANCEMENT ----------------
if st.button("✨ Enhance Resume with AI") and resume_text:
    with st.spinner("Enhancing resume..."):
        enhanced_resume = enhance_resume(resume_text, job_description)
        st.session_state["enhanced_resume"] = enhanced_resume

# ---------------- RESULTS ----------------
if "enhanced_resume" in st.session_state:
    st.header("3️⃣ Enhanced Resume Preview")
    st.text_area("Enhanced Resume", st.session_state["enhanced_resume"], height=300)

    score_after, _ = calculate_ats_score(
        st.session_state["enhanced_resume"], job_description
    )

    st.header("4️⃣ ATS Score Improvement")
    st.metric("ATS Score (After)", f"{score_after}/100", delta=score_after - score_before)
    st.progress(score_after / 100)

# ---------------- FEEDBACK CHAT ----------------
st.header("5️⃣ AI Feedback Chat")

user_question = st.text_input("Ask how to improve your resume further")

if user_question and "enhanced_resume" in st.session_state:
    reply = feedback_chat(user_question, st.session_state["enhanced_resume"])
    st.write(reply)
