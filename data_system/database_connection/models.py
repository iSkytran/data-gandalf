from typing import Optional
from sqlmodel import Field, SQLModel, JSON, Column, String
from sqlalchemy.dialects import postgresql 

class Dataset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic: str
    title: str 
    description: str
    source: str
    url: str
    tags: list[str] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    licenses: list[str] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    col_names: list[str] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    row_count: int
    col_count: int
    entry_count: int
    null_count: int
    usability: float