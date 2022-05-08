from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./wiki.db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
#     # connect args only relevant to sqlite database.
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


Base = declarative_base()