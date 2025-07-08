import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_jobs():
    url="https://remoteok.com/remote-dev-jobs"
    headers={"User-Agent": "Mozilla/5.0"}
    response=requests.get(url,headers=headers)

    soup=BeautifulSoup(response.text,"html.parser")
    jobs=soup.find_all("tr",class_="job")

    job_list=[]
    for job in jobs:
        try:
            title=job.find("h2",{"itemprop": "title"}).text.strip()
            company=job.find("h3",{"itemprop":"name"}).text.strip()
            tag_elements=job.find_all("div",class_="tag")
            tags=[t.find("h3").get_text(strip=True) for t in tag_elements if t.find("h3")]
            link="https://remoteok.com" + job.get("data-href")

            job_list.append({
                "title":title,
                "company":company,
                "tags":", ".join(tags),
                "description":title+" "+" ".join(tags),
                "link": link
            })
        except:
            continue

    df=pd.DataFrame(job_list)
    df.to_csv("scraped_jobs.csv",index=False)
    print("Jobs scraped and saved to scraped_jobs.csv")

