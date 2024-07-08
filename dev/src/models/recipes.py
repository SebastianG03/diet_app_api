from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from models.nutrition_information import NutritionInformation

class RecipeUpdateModel(BaseModel): 
    recipe_name: str = None 
    description: str = None
    nutrition_information: NutritionInformation = None
    ingredients: List[str] = None
    steps: List[str] = None


class RecipeModel(BaseModel):
    id: str = Field(alias='_id') 
    recipe_name: str = Field()
    description: str
    nutrition_information: NutritionInformation
    ingredients: List[str]
    steps: List[str]

class RecipeCollection(BaseModel):
    recipes: List[RecipeModel]