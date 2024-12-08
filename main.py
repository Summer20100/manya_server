from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from typing import Optional, List, Dict, Annotated
from sqlalchemy.orm import Session

from db import session_local, engine, Base
""" from model import Post, User """
from models import Post, User
from schemas import PostResponse, User as DbUser, PostCreate, UserCreate
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:8080/",
    "http://127.0.0.1:8000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


""" Base.metadata.create_all(bind=engine) """

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
        
""" USER """
@app.post("/users/", response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    user = User(name=user.name, age=user.age)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
        
@app.get("/users/", response_model=List[DbUser])
async def get_users(db: Session = Depends(get_db)) -> List[DbUser]:
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@app.get("/users/{user_id}", response_model=DbUser)
async def get_user(user_id: int, db: Session = Depends(get_db)) -> DbUser:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return user

@app.delete("/users/{user_id}", response_model=Dict[str, str])
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> Dict[str, str]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    db.delete(user)
    db.commit()
    return {"message": f"User with ID {user_id} has been deleted"}

""" POST """
@app.post("/posts/", response_model=PostCreate)
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> Post:
    user = db.query(User).filter(User.id == post.author_id).first()
    if user is None:
        return HTTPException(status_code=404, detail='User not found')
    post_create = Post(title=post.title, body=post.body, author_id=post.author_id)
    db.add(post_create)
    db.commit()
    db.refresh(post_create)
    return post_create

@app.get("/posts/", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)) -> List[PostResponse]:
    return db.query(Post).all()




    

















""" users = [
    {'id': 1, 'name': 'Дима', 'age': 40},
    {'id': 2, 'name': 'Кристина', 'age': 35},
    {'id': 3, 'name': 'Лёша', 'age': 42},
]

posts = [
    {'id': 1, 'title': 'News 1', 'body': 'Text 1', 'author': users[2]},
    {'id': 2, 'title': 'News 2', 'body': 'Text 2', 'author': users[0]},
    {'id': 3, 'title': 'News 3', 'body': 'Text 3', 'author': users[1]},
]

@app.get("/items")
async def items() -> List[Post]:
    return [Post(**post) for post in posts]
    # return posts
    
@app.post("/items/add")
async def add_item(post: PostCreate) -> Post:
    author = next(
        (user for user in users if user["id"] == post.author_id), 
        None)
    if not author:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {post.author_id} not found"
        )
    
    print(post.title)
    
    new_post = {
        "id": len(posts) + 1,
        "title": post.title,
        "body": post.body,
        "author": author
    }
    
    # new_post = Post(
    #     id = len(posts) + 1,
    #     title = post.title,
    #     body = post.body,
    #     author = author
    # )
        
    posts.append(new_post)
    
    return Post(**new_post)
    # return new_post

@app.post("/user/add")
async def add_user(user: Annotated[
    UserCreate,
    Body(
        ..., 
        example = {
            "name": "UserName",
            "age": 40
        }
    )
]) -> User:
    new_user = User(
        id = len(users) + 1,
        name = user.name,
        age = user.age
    )
        
    users.append(new_user)
    return new_user
    
@app.get("/items/{id}")
async def items(id: Annotated[int, Path(..., title='ID post here must be', ge=1, )]) -> Post:
    for post in posts:
        if post['id'] == id:
            # return post
            return Post(**post)
    raise HTTPException(status_code=404, detail='Post not found')

@app.get("/search")
async def search( post_id: Annotated[
    Optional[int],
    Query(title='ID post for searching', ge=1 )
]) -> Dict[str, Optional[Post]]:
    if post_id is not None:
        for post in posts:
            if post['id'] == post_id:
                return {'data' : Post(**post)} 
                # return post
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return {'data' : None}
    
    # raise HTTPException(status_code=400, detail="No post id provided") """