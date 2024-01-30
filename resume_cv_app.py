import os
import dotenv
import streamlit as st
from main_functions import get_cover_letter

# Retrieve the OpenAI API key from the environment variable
dotenv.load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Declare the model to use. 
model = 'gpt-3.5-turbo-1106'

# Setting Up The Application Landing Page
st.title("Customized Resume and Cover Letter Builder")
st.markdown("""
        Welcome to a sample application brought to you by the folks at Empowrly.  This is an AI Goal \
        Advisor. It works to help you plan out your professional goals. Please enter your goal below and \
        try it out!    
""")

with st.expander(':red[Disclaimer]'):
    st.write(""" 
            This application is in testing phase only. It is connected to and uses ChatGPT and the OpenAI API. \
            Anything entered here is passed to ChatGPT. Do not input personally identifiable information, \
            confidential information, or anything of the sort. Empowrly is not responsible for the use \
            or outcomes of this publicly used application and you agree to use this at your own risk. 
""")
    
def generate_response(url, cv, model, openai_api_key):
  output = get_cover_letter(url, cv, model, openai_api_key)
  st.write(output)

with st.form('my_form'):
    if openai_api_key == '':
       openai_api_key = st.text_input('OpenAI API Key', 'Enter Your OpenAI API Key', type='password')
    
    text = st.text_area('Enter LinkedIn Job URL:', 'Use the Full Public URL, starting with http://...')
    files = st.file_uploader("Upload files", type=["pdf"], accept_multiple_files=False)
    
    submitted = st.form_submit_button('Submit')
        
    if submitted:
        with st.spinner('Thinking...'):
            generate_response(text, files, model, openai_api_key)