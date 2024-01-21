import streamlit as st
import webbrowser
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
import requests
import json
from google import generativeai as genai
from dotenv import load_dotenv
import requests
import os

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

urls_n_summs = {}

def generate_urls(user_input):
    # You can replace this logic with your own URL generation based on user input
    params = {
        "engine": "google",
        "q": user_input,
        "api_key": os.getenv('SERP_API_KEY'),
        "num" : 8
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]


    organic_results = results.get("organic_results", [])
    links = [result["link"] for result in organic_results]


    return links

def resp(link):
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
    "Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}",
    # "HTTP-Referer": f"{YOUR_SITE_URL}", # Optional, for including your app on openrouter.ai rankings.
    # "X-Title": f"{YOUR_APP_NAME}", # Optional. Shows in rankings on openrouter.ai.
    },
    data=json.dumps({
    "model": "mistralai/mixtral-8x7b-instruct", # Optional
    "messages": [
      {"role": "user", "content": f"""
       Your work is to understand the whole html file and extract usefull information which is seen the person who opens that webpage whose html code is given to you.
       you donot have to get infromation of the code of webpage until specifically asked.
       {requests.get(link).text} this is the html of webpage which a user opens on browser while browsing on internet, you have to generate a summary(word limit=50 words, strictly follow this),
       your summary should be able to explain the person about the website he opens.
       generate summary within wordlimit of 50 words.
       """}
    ]
    })
    )
    return (json.loads(response.text.strip())['choices'][0]['message']['content'])

def geminiresp(url):
    #write code to generate summary from gemini
    model = genai.GenerativeModel('models/gemini-pro')
    response = model.generate_content(f"Give a brief summary in 50 words from this url: {url}")
    return response.text

def search_button_clicked(userinput):
    with st.spinner("Generating URLs..."):
        urls = generate_urls(userinput)
    with st.spinner("Generating summaries..."):
        for url in urls:
            try:
                # summary = resp(url)
                summary = geminiresp(url)
                urls_n_summs[url] = summary
            except:
                continue
            url_button = st.button(summary, on_click=button_click, args=([url]))


def button_click(url):
    webbrowser.open(url, 2)

def main():
    st.title("Streamlit URL Generation with Summary Example")
    st.sidebar.header("User Input")

    # Use st.text_area instead of st.text_input
    user_input = st.sidebar.text_area("Enter your text:")
    generate_button = st.sidebar.button("Generate URLs", on_click=search_button_clicked, args=([user_input]))
    if urls_n_summs:
        for url in urls_n_summs:
            st.button(urls_n_summs[url], on_click=button_click, args=([url]))

if __name__ == "__main__":
    main()
