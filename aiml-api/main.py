from fastapi import FastAPI,Request,HTTPException,UploadFile,File,Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import jwt
import shutil
from jobMatcher import match_resume_to_jobs
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=Path(__file__).parent.parent / "auth" / ".env")
SECRET=os.getenv("JWT_SECRET")
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

@app.post("/recommend_jobs")
async def recommend_jobs(request: Request,file:UploadFile=File(...),top_n: int=Query(5,ge=1,le=10)):
    auth_header=request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401,detail="Unauthorized")
    token=auth_header.replace('Bearer ','')
    try:
        decoded=jwt.decode(token,SECRET,algorithms=['HS256'])
        print("Decoded Token: ",decoded)
        user=decoded['username']
    except Exception as e:
        print("JWT Token error: ",e)
        raise HTTPException(status_code=401,detail='Invalid Token')
    
    resume_dir=Path(__file__).parent.parent / "streamlit" / "resumes"
    # resume_dir.mkdir(parents=True,exist_ok=True)
    file_location = resume_dir / file.filename

    with open(file_location,'wb') as f:
        shutil.copyfileobj(file.file,f)

    try:
        results=match_resume_to_jobs(file_location,top_n=top_n)
        return JSONResponse(content=results.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
