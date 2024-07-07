from typing import List, Optional
from pydantic import BaseModel
from models.ingredients import IngredientsModel
from models.nutrition_information import NutritionInformation

class RecipeUpdateModel(BaseModel): 
    recipe_name: str = None 
    description: str = None
    nutrition_information: NutritionInformation = None
    ingredients: IngredientsModel = None
    steps: list = None


class RecipeModel(BaseModel):
    id: Optional[str] = None 
    recipe_name: str  
    description: str
    nutrition_information: NutritionInformation
    ingredients_ids: List[str]
    steps: list 

class RecipeCollection(BaseModel):
    recipes: List[RecipeModel]