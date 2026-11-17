from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from database import engine,SessionLocal
import models,schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#home
@app.get("/")
def home():
    return{
        "message":"Blog Api Started"
    }

#create blog
@app.post("/blogs",response_model=schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate,db:Session=Depends(get_db)):
    new_blog = models.Blog(
        title = blog.title,
        content = blog.content
        
    )
    db.add(new_blog)
    db.commit()
    db.refresh()
    return new_blog

#read all blog
@app.get("/blogs",response_model=list[schemas.BlogResponse])
def get_blogs(db:Session = Depends(get_db)):
    return db.query(models.Blog).all()
