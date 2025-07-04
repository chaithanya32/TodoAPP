from fastapi import FastAPI

app=FastAPI()

Books=[
    {"title": "Python Crash Course", "author": "Eric Matthes", "language": "Python"},
    {"title": "Learn Python the Hard Way", "author": "Zed A. Shaw", "language": "Python"},
    {"title": "Head First Programming", "author": "David Griffiths, Paul Barry", "language": "Python"},
    {"title": "Think Python", "author": "Allen B. Downey", "language": "Python"},
    {"title": "Programming in C", "author": "Stephen G. Kochan", "language": "C"},
]

@app.get("/")
async def first_api():
    return {"message":"Hello !"}

@app.get("/books")
async def read_all_books():
    return Books

@app.get("/books/{dynamic_parms}")
async def read_all_books(dynamic_params:str):
    return {'dynamic_params':dynamic_params}

    