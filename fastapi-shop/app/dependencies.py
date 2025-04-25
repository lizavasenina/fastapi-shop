"""Module providing access to database session."""

from db.database import session

def get_db():
    """Function returns database session"""
    db = session()
    try:
        yield db
    finally:
        db.close()
