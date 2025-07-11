import streamlit as st
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','aiml-api')))

from loadResume import extract_resume_info

st.set_page_config(layout="wide")
st.title("AI Resume Job Recommender")
st.divider()

if "token" not in st.session_state:
    st.session_state.token=None

if st.session_state.token is None:
    username=st.text_input("Username")
    password=st.text_input("Password",type="password")
    if st.button("Login"):
        res=requests.post("http://localhost:5000/api/login",json={"username":username,"password":password})
        if res.status_code==200:
            st.session_state.token=res.json()["token"]
            st.success("User Logged In")
        else:
            st.error("Incorrect Username or Password")
    st.stop()

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

        try:
            resume_path = os.path.join("resumes", uploaded_file.name)
            files={"file":open(resume_path,"rb")}
            headers={"Authorization":f"Bearer {st.session_state.token}"}
            response=requests.post(f"http://localhost:8000/recommend_jobs?top_n={top_n}",files=files,headers=headers)

            if response.status_code==200:
                jobs=response.json()
                for job in jobs:
                    st.markdown(f"### [{job['title']}]({job['link']}) at {job['company']}")
                    st.write(f"**Tags:** {job['tags']}")
                    st.markdown("---")
            else:
                st.error(f"Failed to Fetch Jobs: {response.status_code}-{response.text}")
        except Exception as e:
            st.error(f"Unkonwn Error: {e}")
    else:
        st.info("Upload a Resume to view Job Recommendations")