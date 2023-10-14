from fastapi import FastAPI
app = FastAPI()

@app.post("/greet/")
def greet_user(name:str):
    return {"message":f"Hello, {name.upper()}! How are you?"}

