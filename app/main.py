from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from . import models, schemas, crud

app = FastAPI(title="URL Shortener API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def health_check():
    return {"message": "URL Shortener API is running"}


@app.post("/api/shorten", response_model=schemas.URLResponse)
def shorten_url(payload: schemas.URLCreate, db: Session = Depends(get_db)):
    return crud.create_short_url(db, payload.original_url)


@app.get("/api/urls", response_model=list[schemas.URLResponse])
def get_urls(db: Session = Depends(get_db)):
    return crud.get_all_urls(db)


@app.get("/r/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_code(db, short_code)
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(url=db_url.original_url)