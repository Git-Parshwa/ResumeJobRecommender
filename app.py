import streamlit as st
from loadResume import extract_resume_info
from jobMatcher import match_resume_to_jobs

st.set_page_config(layout="wide")
st.title("AI Resume Job Recommender")
st.divider()

st.sidebar.title("Controls")
st.sidebar.markdown("Upload your resume on the left and view job matches on the right.")
top_n = st.sidebar.slider("Top N jobs to show", 1, 10, 5)


col1,col_div,col2=st.columns([1,0.1,2])

with col1:
    st.subheader("Upload Resume")
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
        st.success("Resume uploaded!")

with col_div:
    st.markdown(
        """
        <div style="height: 100%; width: 100%; display: flex; justify-content: center;">
            <div style="width: 2px; background-color: lightgray; height: 1000px;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )



with col2:
    st.subheader("Recommended Jobs")
    if uploaded_file:
        st.success("Top Job Recommendations...")
        results=match_resume_to_jobs(f"resumes/{uploaded_file.name}",top_n=top_n)

        for _,row in results.iterrows():
            st.markdown(f"### [{row['title']}]({row['link']}) at {row['company']}")
            st.write(f"**Tags:** {row['tags']}")
            st.markdown("---")
    else:
        st.info("Upload a Resume to view Job Recommendations")