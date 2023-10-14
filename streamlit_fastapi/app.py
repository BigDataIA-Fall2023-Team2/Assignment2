from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import tiktoken
import openai


app = FastAPI()

class RequestModel(BaseModel):
    user_provided_context: str
    user_query: str

class ResponseModel(BaseModel):
    result: str

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
    response.raise_for_status()  # Check for any HTTP errors.
    return response['choices'][0]['message']["content"]

def build_prompt(user_query: str, context: str) -> str:
    return (f"The following is the content from a PDF:\n"
                   f"{context}\n\n"
                   f"Based on the above content, please answer the question below concisely and clearly. "
                   f"If the information isn't available in the content, respond with 'Context not Enough'"
                   f"Ensure the answer is no more than 50 tokens.\n\n"
                   f"Question:\n{user_query}")

@app.get("/ask", response_model=ResponseModel)
def ask(data: RequestModel = Body(...)):
    try:
        context = data.user_provided_context
        user_query=data.user_query
        
        question_prompt = build_prompt(user_query, context)
        response = ask_openai_model(question_prompt)
        return {"result":response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
