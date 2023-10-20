from pypdf import PdfReader
from dotenv import load_dotenv
import streamlit as st
import requests, io, uuid, pathlib, os


env_path = pathlib.Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

fastapi_host = os.getenv('FASTAPI_HOST')


def get_pdf_content_from_link (link : str) -> str:
    file_response = requests.get(file_link)
    file_response.raise_for_status()  # Check for any HTTP errors.
    return file_response.content
    

def extract_pdf_content_using_nougat(content : str, nougat_Server : str) -> (str, int):
    reader = PdfReader(io.BytesIO(content))
    number_of_pages  = len(reader.pages)
    headers = {
        'accept': 'application/json',
        'Bypass-Tunnel-Reminder': 'true',
    }
    extracted_data=""
    num_words = 0
    try:
        for page_num in range(1, number_of_pages+1):
            params = {
            'start': page_num,
            'stop': page_num
            }
            request_counter =0
            random_uuid = uuid.uuid4()
            files = {
            'file': (str(random_uuid) + "_" +str(page_num), file_content, 'application/pdf')
            }
            nougat_response = requests.post(collab_link+"/predict", headers=headers, files=files, params=params)
            if nougat_response.status_code == 200:
                extracted_data = extracted_data + nougat_response.text
                num_words += len(nougat_response.text.split())
            else:
                break
    except Exception as e:
        st.error(e)
        return extracted_data, num_words
    return extracted_data, num_words

def extract_pdf_content_using_pypdf(content : str) -> (str, int):
    extracted_text=""
    num_words=0
    reader = PdfReader(io.BytesIO(content))
    number_of_pages  = len(reader.pages)
    for page_num in range(number_of_pages):
        page = reader.pages[page_num]
        extracted_text += page.extract_text()
        num_words += len(extracted_text.split())
    return extracted_text, num_words
    
def get_answer_from_openai(context : str, user_query : str)->(str, int, int):
    url = fastapi_host + "/ask"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "user_provided_context": context,
        "user_query": user_query
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["result"], response.json()["total_token_used_to_answer_question"], response.json()["total_token_in_context"]
    else:
        return f"Error {response.status_code}: {response.text}" , 0, 0

if 'pdf_content' not in st.session_state:
    st.session_state.pdf_content = ''
    
st.title("")
input_type_option = st.selectbox("How would you like to provide the form to summarize", ('Link', 'Upload a PDF'))
if input_type_option == 'Link':
    file_link = st.text_input("Enter the link to any Securities and Exchange commision form.")
else:
    uploaded_file = st.file_uploader("Upload any Securities and Exchange commision form in pdf format", type=["pdf"])

library_option = st.radio("Select the library to sumamrize your pdf", ('PyPdf', 'Nougat'))
if library_option == 'Nougat':
    st.write("Launch this notebook to generate localtunnel link (https://colab.research.google.com/drive/1p1GjuY8mrnZlx1IsC2F1hvqYusFJPmli?usp=sharing)")
    collab_link = st.text_input("Enter the localtunnel link to google collab running nougat_api.")

if st.button("Submit Pdf"):
    if not hasattr(st.session_state, 'pdf_content') or not st.session_state.pdf_content or not hasattr(st.session_state, 'file_link') or st.session_state.file_link != file_link:
        file_content = None
        if input_type_option == 'Link':
            if file_link != '':
                try:
                    file_content = get_pdf_content_from_link(file_link)
                    st.session_state.file_link=file_link
                except Exception as e:
                    st.error("Error in fetching file from link. Please provide a valid link to any Securities and Exchange commision form.")
                    print(f"Error: {e}")
            else:
                st.error("Please provide a link to any Securities and Exchange commision form or any other downloadable pdf. ")
        else:
            if uploaded_file is not None:
                file_content = uploaded_file.read()
            else:
                st.error("Please upload any Securities and Exchange commision form in pdf format or any other valid pdf.")
        
        if file_content is not None:
            if library_option == 'PyPdf':
                st.session_state.pdf_content, st.session_state.num_words_in_pdf = extract_pdf_content_using_pypdf(file_content)
                st.write("The pdf has been successfully downloaded and parsed using " + library_option)
                st.write("Number of words in the PDF are: " + str(st.session_state.num_words_in_pdf))
            else:
                if collab_link != "":
                    st.session_state.pdf_content, st.session_state.num_words_in_pdf = extract_pdf_content_using_nougat(file_content, collab_link)
                    st.write("The pdf has been successfully downloaded and parsed using " + library_option)
                    st.write("Number of words in the PDF are: " + str(st.session_state.num_words_in_pdf))
                else:
                    st.error("Please provide a localtunnel link to google collab running nougat_api.")


if hasattr(st.session_state, 'pdf_content') and st.session_state.pdf_content:
    user_query = st.text_input("Enter the question you want to ask", key="query_input")
    if st.button("Ask"):
        if user_query:
            st.write(get_answer_from_openai(st.session_state.pdf_content, user_query))

        
        
    
    
    
    
    
    
    
    
    
    
    
