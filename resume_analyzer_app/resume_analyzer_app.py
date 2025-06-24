import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import PyPDF2
from fpdf import FPDF
import io
import os

st.set_page_config(page_title="📄 Resume Analyzer", layout="centered")

# Skill database
SKILLS_DB = [
    "Python", "Java", "C++", "Machine Learning", "Deep Learning", "Data Science",
    "SQL", "Excel", "Communication", "Teamwork", "Problem Solving", "Leadership",
    "HTML", "CSS", "JavaScript", "Power BI", "Tableau", "TensorFlow", "NLP",
    "Node.js", "ReactJS", "Angular", "MongoDB", "MySQL", "Git"
]

# Learning resources
learning_resources = {
    "Python": "https://www.coursera.org/specializations/python",
    "Java": "https://www.codecademy.com/learn/learn-java",
    "C++": "https://www.learncpp.com/",
    "Machine Learning": "https://www.coursera.org/learn/machine-learning",
    "Deep Learning": "https://www.deeplearning.ai/",
    "Data Science": "https://www.coursera.org/specializations/jhu-data-science",
    "SQL": "https://www.kaggle.com/learn/advanced-sql",
    "Excel": "https://www.udemy.com/course/microsoft-excel-2013-from-beginner-to-advanced-and-beyond/",
    "Communication": "https://www.coursera.org/learn/wharton-communication-skills",
    "Teamwork": "https://www.edx.org/course/leading-teams",
    "Problem Solving": "https://www.coursera.org/learn/problem-solving-skills",
    "Leadership": "https://www.edx.org/course/leadership-training",
    "HTML": "https://www.w3schools.com/html/",
    "CSS": "https://www.w3schools.com/css/",
    "JavaScript": "https://www.javascript.com/",
    "Power BI": "https://www.coursera.org/learn/power-bi",
    "Tableau": "https://www.coursera.org/specializations/data-visualization",
    "TensorFlow": "https://www.tensorflow.org/tutorials",
    "NLP": "https://www.coursera.org/learn/language-processing",
    "Node.js": "https://nodejs.dev/en/learn",
    "ReactJS": "https://reactjs.org/",
    "Angular": "https://angular.io/start",
    "MongoDB": "https://www.mongodb.com/learn",
    "MySQL": "https://www.mysqltutorial.org/",
    "Git": "https://www.atlassian.com/git/tutorials"
}

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    return " ".join(page.extract_text() or "" for page in pdf_reader.pages)

def extract_skills_from_text(text):
    return [skill for skill in SKILLS_DB if skill.lower() in text.lower()]

def generate_pdf_report(matched_skills, unmatched_skills, match_percentage):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Resume Analyzer Report", ln=True, align="C")

    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Skill Match Percentage: {match_percentage:.2f}%", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Matched Skills:", ln=True)
    pdf.set_font("Arial", '', 12)
    for skill in matched_skills:
        pdf.cell(200, 10, f"- {skill}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Unmatched Skills:", ln=True)
    pdf.set_font("Arial", '', 12)
    for skill in unmatched_skills:
        pdf.cell(200, 10, f"- {skill}", ln=True)

    temp_path = "resume_report.pdf"
    pdf.output(temp_path)
    with open(temp_path, "rb") as f:
        report_data = f.read()
    os.remove(temp_path)
    return report_data

st.markdown("""
    <h1 style='text-align: center;'>📄 Resume Analyzer</h1>
    <h4 style='text-align: center;'>Match your resume with the job description & get learning recommendations</h4>
    <hr>
""", unsafe_allow_html=True)

resume_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
job_desc = st.text_area("Paste the job description")

if st.button("🔍 Analyze Resume"):
    if resume_file and job_desc:
        resume_text = extract_text_from_pdf(resume_file)
        resume_skills = extract_skills_from_text(resume_text)
        job_skills = extract_skills_from_text(job_desc)

        matched_skills = list(set(resume_skills) & set(job_skills))
        unmatched_skills = list(set(job_skills) - set(resume_skills))

        match_percent = (len(matched_skills) / len(job_skills)) * 100 if job_skills else 0

        col1, col2 = st.columns(2)

        with col1:
            st.success("✅ Matched Skills")
            st.write(matched_skills or "No matches found")
        with col2:
            st.error("❌ Unmatched Skills")
            st.write(unmatched_skills or "All skills matched!")

        st.subheader("📊 Match Percentage")
        st.progress(int(match_percent))
        st.metric(label="Skill Match %", value=f"{match_percent:.2f}%")

        if unmatched_skills:
            st.subheader("📘 Learn these skills")
            for skill in unmatched_skills:
                link = learning_resources.get(skill, f"https://www.google.com/search?q=learn+{skill}")
                st.markdown(f"- **{skill}**: [Click to learn]({link})")

        report_data = generate_pdf_report(matched_skills, unmatched_skills, match_percent)
        st.download_button("📥 Download PDF Report", data=report_data, file_name="resume_report.pdf", mime="application/pdf")
    else:
        st.warning("Please upload a PDF and paste job description first.")
