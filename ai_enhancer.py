from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("sk-xxxxx"))

def enhance_resume(resume_text, job_description):
    prompt = f"""
You are an ATS optimization expert.

Job Description:
{job_description}

Resume:
{resume_text}

Tasks:
- Improve professional tone
- Optimize keywords for ATS
- Rewrite bullet points with action verbs
- Keep content concise and readable

Return ONLY the enhanced resume text.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content


def feedback_chat(question, resume_text):
    prompt = f"""
Resume:
{resume_text}

User question:
{question}

Give clear ATS-focused feedback.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return response.choices[0].message.content
