import os
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from sqlalchemy.future import select
from pydantic import BaseModel

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://movieuser:moviepass@localhost:5432/moviedb")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

class MovieCreate(BaseModel):
    title: str
    description: str | None = None
    year: int

class MovieRead(MovieCreate):
    id: int

app = FastAPI()

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/movies/", response_model=MovieRead)
async def create_movie(movie: MovieCreate, session: AsyncSession = Depends(get_session)):
    db_movie = Movie(**movie.dict())
    session.add(db_movie)
    await session.commit()
    await session.refresh(db_movie)
    return db_movie

@app.get("/movies/", response_model=list[MovieRead])
async def read_movies(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Movie))
    return result.scalars().all()

@app.get("/movies/{movie_id}", response_model=MovieRead)
async def read_movie(movie_id: int, session: AsyncSession = Depends(get_session)):
    movie = await session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.put("/movies/{movie_id}", response_model=MovieRead)
async def update_movie(movie_id: int, movie: MovieCreate, session: AsyncSession = Depends(get_session)):
    db_movie = await session.get(Movie, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in movie.dict().items():
        setattr(db_movie, key, value)
    await session.commit()
    await session.refresh(db_movie)
    return db_movie

@app.delete("/movies/{movie_id}")
async def delete_movie(movie_id: int, session: AsyncSession = Depends(get_session)):
    db_movie = await session.get(Movie, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    await session.delete(db_movie)
    await session.commit()
    return {"ok": True} 