from pydantic import BaseModel

from typing import List, Optional

class Document(BaseModel):
    name: str
    content: str

class Query(BaseModel):
    text: str
    documents: Optional[List[str]] = None