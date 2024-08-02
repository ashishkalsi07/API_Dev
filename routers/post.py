from fastapi import Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from typing import List
import oauth2

router=APIRouter(
    prefix="/posts",
    tags=['posts']
)


@router.get("/",response_model=List[schemas.PostResponse])
def get_data(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    #print(query) will show you it just a sql query which is being written or converted from python to sql
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db), user_id:int = Depends(oauth2.get_current_user)  ):
    new_post = models.Post(owner_id = user_id.id ,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.PostResponse)
def get_posts(id: int,db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id`: {id} does not exist")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int,db: Session = Depends(get_db),user_id:int = Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.PostResponse)
def update_posts(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),user_id:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()