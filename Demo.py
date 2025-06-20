import streamlit as st

import os
from langchain_openai.chat_models import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("SECRET")  
model = "gpt-4.1-nano"



st.title("Streamlit LangChain Demo")

def generate_response(input_text):
    llm = ChatOpenAI(temperature=0.7, api_key=token, model=model)
    st.info(llm.invoke(input_text))

generate_response('hello')
