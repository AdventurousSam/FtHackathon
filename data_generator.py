from google import generativeai as genai
import os
from serpapi import GoogleSearch
import requests
import pandas as pd

def generate_urls(user_input):
    # You can replace this logic with your own URL generation based on user input
    params = {
        "engine": "google",
        "q": user_input,
        "api_key": '392334a4bce04c77f931e52b15ca3820d2939de28cd0e230e876571b507a6019',
        "num" : 20
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    # print(results)

    organic_results = results["organic_results"]


    organic_results = results.get("organic_results", [])
    links = [result["link"] for result in organic_results]


    return links


def get_gemini_response(prompt,input_html,specs):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],input_html,specs])
    return response.text

def get_summary():
    pass
topics_search=['Learn Morse Code',
'Learn to read lips',
'Learn to write in shorthand',
'Buddhist meditation and mudras',
'How to do animation',
'Learn to read body language',
'Learn to read and write poetry',
'Learn to write comedy sketches',
'Basic computer coding',
'Learn to make different breads',
'Learn to make yogurt',
'Update yourself on politics',
'Read feminist theory',
'Why introversion should be more appreciated',
'How to knit',
'What kind of knife to use in what cooking situations',
'What kind of cheese pairs best with what food',
'Learn different knots',
'Learn basic greetings in different languages',
'Speed read the African novel Things Fall Apart',
'Speed read the novel The Good Earth',
'Speed read the novel Malalas Story',
'Speed read or get the digest version of any number of book or short story out there',
'How to perform CPR',
'How to help perform “CPR for mental illnesses”',
'Study how an engine works',
'Learn how to best cut hair',
'Learn how to better appreciate film',
'Learn how to better tell a story',
'Learn how to forage for food',
'Learn how best to garden',
'Learn about different kinds of soon-to-be extinct animals',
'Learn to sleep with your eyes open',
'Learn to recognize constellations',
'Learn to fix clothes',
'Learn to make plastic bag mats',
'Learn to draw',
'Learn to watercolor',
'Learn to paint',
'Study the etymological roots of words']
df=pd.DataFrame()
df['URL']=[]
df['SUMMARY']=[]
count=0
for topic in topics_search:
    urls=generate_urls(topic)
    for url in urls:
        html=requests.get(url).text
        summary=get_summary()
        df.loc[count]=[url,summary]
        count+=1
