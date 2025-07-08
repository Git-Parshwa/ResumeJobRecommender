import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
from loadResume import extract_text_from_pdf

def match_resume_to_jobs(resume_path,jobs_csv="scraped_jobs.csv",top_n=5):
    resume_text=extract_text_from_pdf(resume_path)

    jobs_df=pd.read_csv("scraped_jobs.csv")
    jobs_astext=jobs_df['description'].astype(str).tolist()
    all_text=[resume_text]+jobs_astext

    tfid_vectorizer=TfidfVectorizer(stop_words='english')
    tfid_matrix=tfid_vectorizer.fit_transform(all_text)

    similarities=cosine_similarity(tfid_matrix[0:1],tfid_matrix[1:]).flatten()
    jobs_df["score"]=similarities

    top_jobs=jobs_df.sort_values("score",ascending=False).head(top_n)
    return top_jobs[['title','company','tags','description','link','score']]