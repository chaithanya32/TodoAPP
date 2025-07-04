from typing import Optional
from fastapi import FastAPI ,Path , Query , HTTPException
from pydantic import BaseModel , Field
from starlette import status


app=FastAPI()

class Book:
    id:int
    title:str
    author:str
    description:str
    published_date:int
    rating:int

    def __init__(self,id,title,author,description,published_date,rating):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.published_date=published_date
        self.rating=rating  
        
class BookRequest(BaseModel):
    id:Optional[int]=Field(title='id is not needed')
    title:str=Field(min_length=3)
    author:str=Field(min_length=2)
    description:str=Field(min_length=5,max_length=300)
    published_date:int=Field(gt=1999,lt=2300)
    rating:int=Field(gt=-1,lt=6)

    class Config:
        schema_extra={
            'example':{
                'title':'A new book',
                'author':'codingwithruby',
                'description':'a new book description',
                'published_date':2012,
                'rating':5
            }
        }

BOOKS=[
    Book(1,"Echoes of Eternity","Lena Hartwell","A sweeping tale of love, loss, and redemption set against the backdrop of a timeless realm where memories hold power.",2000,4),
    Book(2,"The Quantum Paradox","Dr. Raj Mehra","A thrilling sci-fi adventure where a physicist uncovers a conspiracy that could unravel the fabric of the universe.",2010,5),
    Book(3,"Whispers in the Fog","Clara Voss","A chilling mystery unfolds as a detective in a sleepy coastal town unearths secrets long buried in mist and silence.",2020,4),
    Book(4,"The Alchemist's Key","Julian Blake","In a medieval world of magic and alchemy, a young apprentice must decode an ancient key to prevent a dark prophecy.",2015,5),
    Book(5,"Canvas of the Soul","Isabelle Monroe","An introspective journey through art, emotion, and healing, told through the life of a reclusive painter rediscovering herself.",2004,3),

]

@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_book(book_id:int=Path(gt=0)):
    for book in BOOKS:
        if book.id==book_id:
            return book
    raise HTTPException(status_code=404,detail='Item not found')

# assignment 
@app.get("/books/publish/",status_code=status.HTTP_200_OK)
async def read_book(book_publishedDate:int=Query(gt=1999,lt=2300)):
    books_list=[]
    for book in BOOKS:
        if book.published_date==book_publishedDate:
            books_list.append(book)
        
    return books_list 


@app.get("/books/",status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating:int=Query(gt=0,lt=6)):
    book_to_return=[]
    for book in BOOKS:
        if book.rating == book_rating:
            book_to_return.append(book)
    
    return book_to_return


@app.post("/create_book",status_code=status.HTTP_201_CREATED)
async def  create_book(book_request:BookRequest):
    new_book=Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))

    
def find_book_id(book:Book):
    if len(BOOKS) > 0:
        book.id=BOOKS[-1].id+1
    else:
        book.id=1

    return book

@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book:BookRequest):
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book.id:
            BOOKS[i]=book
            book_changed=True
    if not book_changed:
        HTTPException(status_code=404,detail='item not found')
        
@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int=Path(gt=0)):
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            BOOKS.pop(i)
            book_changed=True
            break
    if not book_changed:
        HTTPException(status_code=404,detail='item not found')
        