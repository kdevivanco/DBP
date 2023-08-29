from pydantic import BaseModel

class AnimeModel(BaseModel):
    id: int
    title: str
    poster: str
    categoria: str
    rating: float
    descripcion: str


