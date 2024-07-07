from typing import List, Optional
from pydantic import BaseModel

class IngredientsUpdateModel(BaseModel):
    name: Optional[str] = None


class IngredientsModel(BaseModel):
    id: Optional[str] = None 
    name: str 
    
class IngredientsCollection(BaseModel):
    ingredients: List[IngredientsModel]