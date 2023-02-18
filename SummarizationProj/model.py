from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel
from database import BASE

class SummarizationTable(BASE):
    __tablename__ = "travel"
    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    nearest = Column(String, nullable=False)
    rank = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    time = Column(Float, nullable=True)
    name = Column(String(120), nullable=False)


class Travel(BaseModel):
    id: int
    latitude: float
    longitude: float
    nearest: str
    rank: int
    category: str
    time: float
    name: str


class Input(BaseModel):
    url : str
    text : str