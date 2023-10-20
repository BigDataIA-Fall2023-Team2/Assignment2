# Assignment-2 (Text summarization app)

### Project Descrition 

This project builds upon the foundation laid by Project 1(https://github.com/BigDataIA-Fall2023-Team2/Assignment1/blob/main/part1/Readme.md), leveraging the text extracted from PDF documents to facilitate summarization and question answering. Within our application, users can pose questions pertaining to the content of the PDF, to which the app will provide insightful responses. Utilizing OpenAI APIs, we extract and analyze the text to generate accurate answers.

A distinctive feature of our application is the implementation of a chunk-based data processing approach. By segmenting the text data into manageable chunks, we enhance the efficiency of the query process. If an answer is found within a particular chunk, there's no need to process the remaining text, thereby optimizing resource utilization and expediting response times. Through this focused, chunk-driven methodology, we aim to deliver a robust and responsive user experience that makes interacting with textual data both intuitive and insightful. 

### Application and Documentation Link

App link - https://team2assignment2.streamlit.app/

Fast API hosted on Railway link - https://team2assignment2.up.railway.app/docs

### Project Resources

Google Codelab link - https://codelabs-preview.appspot.com/?file_id=1OEvGnQV7FttHE2BCg1mvAkjxIKbMMB9NSFUwHtGoqcA#0

Google Collab Notebook link - 

### Tech Stack
Python | Streamlit | Google Collab | Nougat | Railway | Fast API

### Architecture diagram ###
![image](https://github.com/BigDataIA-Fall2023-Team2/Assignment2/assets/131703516/127ca5a6-520a-4730-8263-0c5931941ae3)

### Project Flow
The application allows users to upload a file or provide a link, after which they can choose between 'Nougat' and 'PyPDF' for processing. If 'Nougat' is selected, the user must provide a Google Collab localtunnel link. Streamlit then parses the PDF using the chosen method (Nougat or PyPDF). Users can subsequently pose questions about the extracted text. Upon receiving a question, Streamlit communicates with FastAPI, sending both the text and the query. FastAPI then breaks down the data into smaller chunks and sequentially queries OpenAI for an answer from each chunk until a satisfactory answer is located.

### Repository Structure

![image](https://github.com/BigDataIA-Fall2023-Team2/Assignment2/assets/131703516/c73c2c95-4355-47c0-befe-1e3e91313fc9)

### Contributions

| Name                            | Contribution                               |  
| ------------------------------- | -------------------------------------------|
| Chinmay Gandi                   | Embeddings, demo replication in ipynb      |
| Dhawal Negi                     | Fast API, Railway, Streamlit, Text Chunking|
| Shardul Chavan                  | Fine Tuning,  demo replication in ipynb    | 


### Additional Notes
WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK. 
