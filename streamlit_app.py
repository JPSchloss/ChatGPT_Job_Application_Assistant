import streamlit as st
from llm_functions import run_llm, get_cover_letter, get_resume_improvements

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

model = 'gpt-3.5-turbo-1106'

def generate_response(url, cv, model, openai_api_key, temperature, cv_improvements, cover_letter):
  
  pdf_qa = run_llm(url, cv, model, openai_api_key, temperature)

  if cv_improvements:
      output = get_resume_improvements(pdf_qa)
      with st.container():
        st.subheader('Potential CV Improvements:')
        st.write(output['result'])
        st.divider()
      
  if cover_letter:
      output = get_cover_letter(pdf_qa)
      with st.container():
        st.subheader('Generated Cover Letter:')
        st.write(output['result'])
        st.divider()

  return
  

def main():

  try:
     # Retrieve the OpenAI API key from the environment variable
      openai_api_key = st.secrets["OPENAI_API_KEY"]
  except:
      openai_api_key = ''
     
  
  st.sidebar.subheader('Choose Model Function:')
  cv_improvements = st.sidebar.checkbox('CV Suggestions', value=True)
  cover_letter = st.sidebar.checkbox('Cover Letter Generator', value=True)

  if openai_api_key == '':
        st.sidebar.subheader('Enter OpenAI API Key:')
        openai_api_key = st.sidebar.text_input('OpenAI API Key', '', type='password')
  
  st.sidebar.subheader('Set Model Temperature:')
  temperature = st.sidebar.slider("Model Temperature", 0.0, 2.0, step=0.1, value=0.3)
  
  st.title('Job Application Assistant')
  st.markdown(''' \
          Welcome to the Job Application Assistant! \n\n\
          The way this application works is by taking a LinkedIn Public Job Posting URL \n\
          and a PDF copy of your CV to generate suggestions on how to \n\
          improve your CV and/or to generate a tailored cover letter for the job. \n\n\
          Please fill out the fields on this page and hit submit when ready! \n\n\
          ''')
  
  with st.expander(':red[Disclaimer]'):
    st.write(""" 
            This application is offered as a free tool. It is connected to and uses ChatGPT and the OpenAI API. \
            Anything entered here is passed to ChatGPT. Do not input personally identifiable information, \
            confidential information, or anything of the sort. The creator of this tool is not responsible for the use \
            or outcomes of this publicly used application and you agree to use this at your own risk. 
            """)
  
  
  with st.form('my_form'):
      text = st.text_area('Enter LinkedIn Job URL:', '')
      files = st.file_uploader("Upload Files:", type=["pdf"], accept_multiple_files=False)
      
      submitted = st.form_submit_button('Submit')
          
  if submitted:
      if openai_api_key != '' and openai_api_key.startswith('sk-'):
        if text != '':
          if files != None:
            #try:
              with st.spinner('Please wait for the model to load. This may take a minute...'):
                generate_response(text, files, model, openai_api_key, temperature, cv_improvements, cover_letter)
            # except:
            #    st.error('An Error Occured With The Model! Please Try Again', icon="🚨")
          else:
             st.warning('There may be a problem. Please Check Your Uploaded File.', icon='⚠')
        else:
          st.warning('There may be a problem. Please Check Your URL.', icon='⚠')
      else:
        st.warning('There may be a problem. Please Check Your OpenAI API Key.', icon='⚠')
  return

if __name__ == "__main__":
   main()