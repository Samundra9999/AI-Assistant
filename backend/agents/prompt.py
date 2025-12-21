from pydantic import BaseModel, Field
from typing import Literal, Annotated, List

class Question(BaseModel):
    question : Annotated[List[str],Field(description="List of all Questions from paper")]

