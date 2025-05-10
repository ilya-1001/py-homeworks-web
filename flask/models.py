import datetime
import os
from atexit import register

from sqlalchemy import DateTime, Integer, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

POSTGRES_USER = os.getenv("POSTGRES_USER", "app")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1234")
POSTGRES_DB = os.getenv("POSTGRES_DB", "netology")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")


PG_DSN = (
    f"postgresql://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):

    @property
    def id_dict(self):
        return {"id": self.id}


class Ad(Base):

    __tablename__ = "ads"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    date_of_creation: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    owner: Mapped[str] = mapped_column(String, nullable=False)

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date_of_creation": self.date_of_creation.isoformat(),
            "owner": self.owner,
        }


Base.metadata.create_all(bind=engine)
register(engine.dispose)
