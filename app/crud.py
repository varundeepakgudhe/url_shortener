import random
import string
from sqlalchemy.orm import Session
from . import models


def generate_short_code(length: int = 6) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def create_short_url(db: Session, original_url: str):
    short_code = generate_short_code()

    # avoid duplicate short codes
    while db.query(models.ShortURL).filter(models.ShortURL.short_code == short_code).first():
        short_code = generate_short_code()

    db_url = models.ShortURL(
        original_url=original_url,
        short_code=short_code
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_url_by_code(db: Session, short_code: str):
    return db.query(models.ShortURL).filter(models.ShortURL.short_code == short_code).first()


def get_all_urls(db: Session):
    return db.query(models.ShortURL).all()