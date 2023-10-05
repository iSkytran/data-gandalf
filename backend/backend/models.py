from typing import Optional
from sqlmodel import Field, SQLModel

class Dataset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic: str
    name: str
    description: str
    source: str
    tags: Optional[str]
    percent_null: Optional[int]
    column_count: Optional[int]
