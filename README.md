# Assignment-2 (Text summarization app)

### Project Descrition 

The project is an extension of the prevous project 1 (https://github.com/BigDataIA-Fall2023-Team2/Assignment1/blob/main/part1/Readme.md). In this project, the text that is extracted from pdf using project 1 is used for summarization/question answering. The user will ask respective questions related to the pdf in the application, and the app will be respond to the questions. We will be using openAI APIs to fetch result from the extracted text. 

The most important feature of our application is that we will be sending data in chunks so that if openAI is able to find an answer to a question in a particular chunk then the rest of the text in the pdf would not be required for further analysis. 

### Application and Documentation Link

App link - https://team2assignment2.streamlit.app/

Fast API hosted on Railway link - https://team2assignment2.up.railway.app/docs

### Project Resources

Google Codelab link - 

### Tech Stack
Python | Streamlit | Google Collab | Nougat | Railway | Fast API

### Architecture diagram ###
![image](https://github.com/BigDataIA-Fall2023-Team2/Assignment2/assets/131703516/f6f34043-b073-4aea-9950-eb25e35df4bf)

### Project Flow
The user will upload the pdf in our streamlit application. The user has to then open the mentioned google colab notebook and paste the output URL which is generated in the colab notebook in the streamlit app. The colab notebook will extract the text from pdf and pass to streamlit application. Now, the extracted text and the question asked by user is passed to chatgpt api but it is not passed directly. It will first go through a fast api service that has been deployed on railway. This interaction will happen between railway and chatgpt.

### Repository Structure

![image](https://github.com/BigDataIA-Fall2023-Team2/Assignment2/assets/131703516/33355c85-8d75-471c-bfac-396672bf0ede)



### Contributions
