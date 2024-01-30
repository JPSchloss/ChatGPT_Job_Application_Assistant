from langchain_openai import OpenAIEmbeddings # Updated Embedding Package Here... Causes problems otherwise. (UUID cannot be imported.)
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from main_functions import load_pdf, extract_text_from_url, split_text_documents


def run_llm(url, pdf, model, openai_api_key, temperature):
    pdf_doc = load_pdf(pdf)
    job_post = extract_text_from_url(url)

    pdf_doc.extend(job_post)
    documents = split_text_documents(pdf_doc)

    vectordb = Chroma.from_documents(documents, embedding=OpenAIEmbeddings(openai_api_key = openai_api_key))

    llm = ChatOpenAI(temperature=temperature, model_name=model, openai_api_key = openai_api_key)

    pdf_qa = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever(search_kwargs={'k': 4}),
        chain_type="stuff",
    )
    
    return pdf_qa

def get_cover_letter(pdf_qa):

    query = """ Write a cover letter for given CV and Job posting. You are passed a \
                CV and a job description. Use only information in the CV as examples to put into \
                the Cover Letter. Relate the examples you choose to the skills discussed in the \
                job description, but DO NOT use the job description as a source for examples for the \
                Cover Letter. Follow the template outlined below for the appearance of the returned \
                result. It is up to you to generate the text for the BODY. This should be 4-6 paragraphs. \
                Use an intelligent but conversational style for your response and prioritize more recent experience in the CV.\
                Sign the letter in the NAME FROM CV section with the name extraced from the CV passed to you.
                
                Template: 
                Dear Hiring Manager, 
                [BODY]
                Thank you, 
                [NAME FROM CV]
                """

    result = pdf_qa.invoke(query)

    return result

def get_resume_improvements(pdf_qa):
    
    query = """ Using the attached Job Posting, can you identify the keywords and most important skills highlighted \
                in the Job Posting? Can you then use those keywords and highlighted skills to identify what elements \
                of the attached CV should be highlighted more than others. Can you also highlight what elements should \
                be downplayed or minimized that fall out of the scope of the Job Posting? \
                
                You are passed a CV and a job description. Use the job description as a guide to \
                identify improvements that could be made to the CV. Improvements can include, but are \
                not limited to, mentioning certain skills present in the job description that are not present in \
                the CV, and highlighting experiences that would better align with the \
                job description. You should provide 3-10 recommendations in your responses. 
                
                Template:
                Main Skills In Job Posting:
                [KEYWORDS AND IMPORTANT SKILLS]
                
                Things To Highlight In Your CV:
                [THING IN CV TO HIGHLIGHT]
                
                Things To Get Rid Of In Your CV:
                [THINGS TO REMOVE IN CV]
                """
    
    result = pdf_qa.invoke(query)

    return result


