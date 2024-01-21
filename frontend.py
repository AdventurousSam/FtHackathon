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



def button_click(url):
    webbrowser.open(url,1)

def main():
    st.title("Streamlit URL Generation with Summary Example")
    st.sidebar.header("User Input")

    # Use st.text_area instead of st.text_input
    user_input = st.sidebar.text_area("Enter your text:")

    # Check if Enter key is pressed before generating URLs
    if st.sidebar.button("Generate URLs"):
        urls = generate_urls(user_input)
        # print("\n\n\ndone\n\n\n")
        st.header("Generated Summaries:")
        for url in urls:
            try:
                summary = resp(url)
            except:
                continue
            button = st.button(summary, on_click=button_click, args=([url]))




if __name__ == "__main__":
    main()
