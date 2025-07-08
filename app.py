import streamlit as st
from loadResume import extract_resume_info
from jobMatcher import match_resume_to_jobs

st.title("AI Resume Job Recommender")
uploaded_file=st.file_uploader("Upload your Resume(PDF)",type=["pdf"])

if uploaded_file:
    with open(f"resumes/{uploaded_file.name}","wb") as f:
        f.write(uploaded_file.read())

    resume_info=extract_resume_info(f"resumes/{uploaded_file.name}")

    st.subheader("📄 Resume Summary")
    st.write(f"**Name:** {resume_info['name']}")
    st.write(f"**Email:** {resume_info['email']}")
    st.write(f"**Phone:** {resume_info['phone']}")
    st.write(f"**Skills:** {', '.join(resume_info['skills'])}") 

    st.success("Resume uploaded! Top Job Recommendations...")
    results=match_resume_to_jobs(f"resumes/{uploaded_file.name}")

    for _,row in results.iterrows():
        st.markdown(f"### [{row['title']}]({row['link']}) at {row['company']}")
        st.write(f"**Tags:** {row['tags']}")
        st.markdown("---")