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
        "num" : 5
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]


    organic_results = results.get("organic_results", [])
    links = [result["link"] for result in organic_results]


    return links

def scrape_url(url,specs='general information'):
    x=requests.get(url)
    prompt=[f"""
            Hey you are expert in understanding about the website and creating a short summary within a word limit of 50 words.
            You will be given a url you can also open that url for getting me information.
            you donot have to give any imformation about the code of the website unless asked specifically.
        """]
    # response=get_gemini_response(prompt,str(url),specs)
    return url
def get_gemini_response(prompt,input_html,specs):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],input_html,specs])
    return response.text


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
            # summary = scrape_url(url)
            button = st.button(url, on_click=button_click, args=([url]))




if __name__ == "__main__":
    main()
