from typing import Optional
from sqlmodel import Field, SQLModel, Column, JSON

class Dataset(SQLModel, table=True):
    """Schema for a dataset.

    Contains a unique identifier and relevant metadata
    for a dataset.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    topic: str
    title: str 
    description: str
    url: str
    source: str
    tags: str = Field(sa_column=Column(JSON))
    licenses: str = Field(sa_column=Column(JSON))
    col_names: str = Field(sa_column=Column(JSON))
    col_count: int
    row_count: int
    entry_count: int
    null_count: int
    usability: float

class RatingBase(SQLModel):
    """Model for a user rating a recommendation.

    Attributes:
        id: Primary key for the entry.
        recommend: A boolean where true is the user likes the recommendation.
            The recommendation while false means it's not a good recommendation.
        user_session: UUID of a tracked user session.
        source_dataset: The dataset that a user has selected.
        destination_dataset: The dataset that was recommended for
            the source dataset.
    """
    user_session: str
    recommend: bool
    source_dataset: int = Field(foreign_key="dataset.id")
    destination_dataset: int = Field(foreign_key="dataset.id")

class Rating(RatingBase, table=True):
    """Table schema for a recommendation including the primary key.
    Inherits from RatingBase.

    Attributes:
        id: Primary key for the entry.
    """
    id: Optional[int] = Field(default=None, primary_key=True)

