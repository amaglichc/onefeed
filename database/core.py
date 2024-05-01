from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import get_url_for_db

engine = create_engine(url=get_url_for_db(), echo=True)
sessionmaker = sessionmaker(bind=engine)
Base = declarative_base()


def init_db() -> None:
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn)
