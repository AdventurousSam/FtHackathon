from google import generativeai as genai
import os
from serpapi import search
import requests
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
def generate_urls(user_input):
    # You can replace this logic with your own URL generation based on user input
    params = {
        "engine": "google",
        "q": user_input,
        "api_key": '392334a4bce04c77f931e52b15ca3820d2939de28cd0e230e876571b507a6019',
        "num" : 20
    }

    searh = search(params)
    results = searh.as_dict()
    # print(results)

    organic_results = results["organic_results"]


    organic_results = results.get("organic_results", [])
    links = [result["link"] for result in organic_results]


    return links


def get_gemini_response(input_html):
    safety_settings = {
        'HARM_CATEGORY_SEXUALLY_EXPLICIT' : 'block_none',
        'HARM_CATEGORY_HATE_SPEECH' : 'block_none',
        'HARM_CATEGORY_HARASSMENT' : 'block_none',
        'HARM_CATEGORY_DANGEROUS_CONTENT' : 'block_none'
    }
    gen_config = genai.GenerationConfig(temperature=0.8)

    model = genai.GenerativeModel(
        'models/gemini-pro',
        safety_settings=safety_settings,
        generation_config=gen_config
        )
    chat = model.start_chat()

    response = chat.send_message("I have the html of a webpage. Since I can't send you all of it in one prompt, I'll give in pieces from the next prompt. When I've sent all, I'll tell you, You are supposed to give me a summary within 150 words of what information is given on that webpage. is that ok?")

    n = len(html)
    for i in range(0, n, 120000):
        resp = chat.send_message(input_html[i:i+120000])
        # print(resp.text)
    final_response = chat.send_message("I've sent you all the html content, Now give me a summary of what that webpage is about(word limit=150), i want summary in form of a paragraph.")
    # print("final: ", final_response.text)
    # response=model.generate_content([prompt[0],input_html,specs])
    return final_response.text

def get_summary():
    pass
topics_search=[
    # 'Learn Morse Code',
# 'Learn to read lips',
# 'Learn to write in shorthand',
# 'Buddhist meditation and mudras',
# 'How to do animation',
# 'Learn to read body language',
# 'Learn to read and write poetry',
# 'Learn to write comedy sketches',
# 'Basic computer coding',
# 'Learn to make different breads',
# 'Learn to make yogurt',
# 'Update yourself on politics',
# 'Read feminist theory',
# 'Why introversion should be more appreciated',
# 'How to knit']
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
'Learn how to forage for food']
# 'Learn how best to garden',
# 'Learn about different kinds of soon-to-be extinct animals',
# 'Learn to sleep with your eyes open',
# 'Learn to recognize constellations',
# 'Learn to fix clothes',
# 'Learn to make plastic bag mats',
# 'Learn to draw',
# 'Learn to watercolor',
# 'Learn to paint',
# 'Study the etymological roots of words']
# df=pd.read_csv('data_g_sim.csv')
df=pd.DataFrame()
df['URL']=[]
df['SUMMARY']=[]
count=0
for topic in topics_search:
    urls=generate_urls(topic)
    print(topic)
    for url in urls:
        print(url)
        html=requests.get(url).text
        try:
            summary=get_gemini_response(input_html=html)
        except:
            continue
        df.loc[count]=[url,summary]
        df.to_csv('data_g_sam1.csv')
        count+=1
        # break
    # break
# print(df)
df.to_csv('data_g_sam.csv')
# print(len(requests.get('https://deepmind.google/technologies/gemini/#introduction').text))
