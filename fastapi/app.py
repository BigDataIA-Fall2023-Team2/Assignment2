from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import tiktoken
import openai
import uvicorn


app = FastAPI()

class RequestModel(BaseModel):
    user_provided_context: str
    user_query: str

class ResponseModel(BaseModel):
    result: str
    total_token_used_to_answer_question: int
    total_token_in_context: int
    
def chunk_context(s, max_words=300) -> list:
    sentences = s.split('. ')
    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        sentence_word_count = len(sentence.split())
        if current_word_count + sentence_word_count > max_words:
            chunks.append('. '.join(current_chunk))
            current_chunk = []
            current_word_count = 0
        current_chunk.append(sentence)
        current_word_count += sentence_word_count
    if current_chunk:
        chunks.append('. '.join(current_chunk))
    return chunks

def num_tokens_from_string(string: str) -> int:
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(string))
    return num_tokens

def ask_openai_model(prompt: str)-> str:
    openai.api_key = "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"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    return response['choices'][0]['message']["content"]

def build_prompt(user_query: str, context: str) -> str:
    return (f"The following is the content from a PDF:\n"
                   f"{context}\n\n"
                   f"Based on the above content, please answer the question below concisely and clearly. "
                   f"If the information isn't available in the content, just respond with 'Context not Enough' and do not specify anything else"
                   f"If found, Ensure the answer is no more than 50 tokens.\n\n"
                   f"Question:\n{user_query}")

@app.post("/ask", response_model=ResponseModel)
def ask(data: RequestModel = Body(...)):
    context = data.user_provided_context
    user_query=data.user_query
    total_token_in_context = num_tokens_from_string(context)
    context_chunks = chunk_context(context, 200)
    total_token_used_to_answer_question = 0
    for context_chunk in context_chunks:
        question_prompt = build_prompt(user_query, context_chunk)
        print(num_tokens_from_string(question_prompt))
        total_token_used_to_answer_question += num_tokens_from_string(question_prompt)
        response = ask_openai_model(question_prompt)
        print(response)
        if not response.lower().__contains__("context not enough"):
            print("hello")
            return {
                        "result":response,
                        "total_token_used_to_answer_question":total_token_used_to_answer_question,
                        "total_token_in_context":total_token_in_context
                    }
    return {
        "result":"Suitable answer not found for your question.",
        "total_token_used_to_answer_question":total_token_used_to_answer_question,
        "total_token_in_context":total_token_in_context
    }
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)