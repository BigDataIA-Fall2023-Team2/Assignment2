import streamlit as st
import requests, io, uuid
from pypdf import PdfReader


def get_pdf_content_from_link (link : str) -> str:
    file_response = requests.get(file_link)
    file_response.raise_for_status()  # Check for any HTTP errors.
    return file_response.content
    
def extract_pdf_content_using_nougat(content : str, nougat_Server : str) -> str:
    reader = PdfReader(io.BytesIO(content))
    number_of_pages  = len(reader.pages)
    headers = {
        'accept': 'application/json',
        'Bypass-Tunnel-Reminder': 'true',
    }
    extracted_data=""
    num_words = 0
    for page_num in range(1, number_of_pages+1):
        params = {
        'start': page_num,
        'stop': page_num
        }
        request_counter =0
        while request_counter < 3:
            random_uuid = uuid.uuid4()
            files = {
            'file': (str(random_uuid) + "_" +str(page_num), file_content, 'application/pdf')
            }

            nougat_response = requests.post(collab_link+"/predict", headers=headers, files=files, params=params)
            if nougat_response.status_code == 200:
                extracted_data = extracted_data + nougat_response.text
                num_words += len(nougat_response.text.split())
                break
            else:
                print("Request failed with status code:" + str(nougat_response.status_code))
                print(nougat_response.text)
                request_counter += 1
    return extracted_data
    
def get_answer_from_openai(context : str, user_query : str)->str:
    url = "http://127.0.0.1:8000/ask"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "user_provided_context": context,
        "user_query": user_query
    }
    response = requests.get(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["result"]
    else:
        return f"Error {response.status_code}: {response.text}"

    
st.title("FastAPI and Streamlit Interaction")

file_link = st.text_input("Enter the link to any Securities and Exchange commision form.")
st.write("Launch this notebook to generate localtunnel link (https://colab.research.google.com/drive/1p1GjuY8mrnZlx1IsC2F1hvqYusFJPmli?usp=sharing)")
collab_link = st.text_input("Enter the localtunnel link to google collab running nougat_api.")
user_query = st.text_input("Enter the question you want to ask")

if st.button("Run "):
    file_content = get_pdf_content_from_link(file_link)
    pdf_content = extract_pdf_content_using_nougat(file_content, collab_link)
    st.write(get_answer_from_openai(pdf_content, user_query))
        
    
    
    
    
    
    
    
    
    
    
