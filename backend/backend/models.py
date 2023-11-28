from typing import Optional
from sqlmodel import Field, SQLModel, Column, JSON

class Dataset(SQLModel, table=True):
    """Schema for a dataset.

    Contains a unique identifier and relevant metadata
    for a dataset.

    Attributes:
        id (int, Optional): Primary key for the entry.
        topic (str): The topic of the dataset.
        title (str): The title of the dataset.
        description (str): A description of the dataset. 
        url (str): The url of where the dataset came from.
        source (str): The source of the dataset.
        tags (str): JSON formatted field containing the tags of the dataset.
        licenses (str): JSON formatted field containing the licenses for the dataset.
        col_names (str): JSON formatted field containing the name of the columns
            in the dataset.
        col_count (int): The number of columns in the dataset.
        row_count (int): The number of rows in the dataset.
        entry_count (int): The number of entries in the dataset.
        null_count (int): The number of empty entries in the dataset.
        usability (float): A score representing the usability of the dataset.
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
        recommend (bool): A boolean where true is the user likes the recommendation.
            The recommendation while false means it's not a good recommendation.
        user_session (str): UUID of a tracked user session.
        source_dataset (int): The dataset that a user has selected.
        destination_dataset (int): The dataset that was recommended for
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
        id (int, Optional): Primary key for the entry.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
