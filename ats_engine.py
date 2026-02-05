import re

def extract_keywords(text):
    text = text.lower()
    words = re.findall(r"[a-zA-Z]+", text)
    return set(words)

def calculate_ats_score(resume_text, job_description):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_description)

    if not jd_keywords:
        return 40, []

    matched = resume_keywords.intersection(jd_keywords)
    match_ratio = len(matched) / len(jd_keywords)

    # Keyword score (70%)
    keyword_score = match_ratio * 70

    # Section score (30%)
    sections = ["experience", "skills", "education", "projects"]
    section_score = sum(1 for s in sections if s in resume_text.lower()) * 7.5

    final_score = min(100, int(keyword_score + section_score))

    missing_keywords = list(jd_keywords - resume_keywords)[:10]

    return final_score, missing_keywords
