from typing import List, Optional
from pydantic import BaseModel
from dev.src.models.ingredients import IngredientsModel
from dev.src.models.nutrition_information import NutritionInformation

class RecipeUpdateModel(BaseModel):
    id: str 
    recipe_name: str = None 
    description: str = None
    nutrition_information: NutritionInformation = None
    ingredients: IngredientsModel = None
    steps: list = None


class RecipeModel(BaseModel):
    id: str 
    recipe_name: str  
    description: str
    nutrition_information: NutritionInformation
    ingredients_ids: List[str]
    steps: list 

class RecipeCollection(BaseModel):
    recipes: List[RecipeModel]