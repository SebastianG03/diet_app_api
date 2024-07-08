

from typing import List
from prediction.user_data import UserData
from models.recipes import RecipeModel


def recomendate_recipes(recipes: List[RecipeModel], user_data: UserData) -> List[RecipeModel]:
    filtered_recipes = []
    actual_calories = 0.0
    for recipe in recipes:
        nutrition_info = recipe.nutrition_information
        TMB = user_data.calculate_TMB()
        can_recommend = user_data.calculate_calories_by_macronutrients(
            carbs=nutrition_info.total_carbohydrates,
            fats=nutrition_info.total_fats,
            proteins=nutrition_info.protein
        )
        if can_recommend and actual_calories < TMB:
            actual_calories += nutrition_info.calories
            filtered_recipes.append(recipe)
    
    return filtered_recipes