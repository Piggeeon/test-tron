from sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base

class DatabaseCore:
    def __init__(self, url: URL):
        self.url = url
        self.engine = create_engine(url, echo=True)
        self.session_factory = sessionmaker(bind=self.engine)

    def get_session(self):
        db = self.session_factory()
        try:
            yield db
        finally:
            db.close()


    def create_tables(self):
        Base.metadata.create_all(bind=self.engine, checkfirst=True)
