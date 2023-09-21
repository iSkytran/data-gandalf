from typing import Optional, List
from sqlmodel import Field, SQLModel, JSON

class Dataset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic: str
    title: str 
    description: str
    tags: List[str] = Field(sa_column=JSON)
    licenses: List[str] = Field(sa_column=JSON)
    percent_null: float 
    row_count: int
    col_count: int