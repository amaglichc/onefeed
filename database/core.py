from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from config import get_url_for_db

engine = create_async_engine(url=get_url_for_db(), echo=True)
sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


def init_db() -> None:
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn)
