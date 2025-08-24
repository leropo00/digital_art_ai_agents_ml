import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator

load_dotenv()
engine = create_async_engine(os.getenv("DATABASE_URI"), echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
