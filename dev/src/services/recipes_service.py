from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument

from dev.src.data.database_connection import DatabaseConnection
from ..models import recipes

recipes_router = APIRouter()
connection = DatabaseConnection()
recipes_collection = connection.connect_collection(collection='recipes') 
root = "/api/recipes/"

@recipes_router.post(
    root,
    response_description="Add a new recipe",
    response_model=recipes.RecipeModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_recipe(recipe: recipes.RecipeModel):
    """
    Insert a new recipe.
    A unique `id` will be created and provided in the response.
    """
    new_recipe = await recipes_collection.insert_one(
        recipe.model_dump(by_alias=True, exclude=["id"])
    )
    created_recipe = await recipes_collection.find_one(
        {"_id": new_recipe.inserted_id}
    )
    return created_recipe

@recipes_router.get(
    root,
    response_description="List all recipes",
    response_model=recipes.RecipeCollection,
    response_model_by_alias=False,
)
async def list_recipes():
    """
    List all of the recipes data in the database.
    """
    return recipes.RecipeCollection(recipes==await recipes_collection.find().to_list(100))


@recipes_router.get(
    root + "{id}",
    response_description="Get a single recipe",
    response_model=recipes.RecipeModel,
    response_model_by_alias=False,
)
async def show_recipe(id: str):
    """
    Get the record for a specific Recipe, looked up by `id`.
    """
    if (
        recipe := await recipes_collection.find_one({"_id": id})
    ) is not None:
        return recipe
    raise HTTPException(status_code=404, detail=f"Recipe {id} not found")



@recipes_router.put(
    root + "{id}",
    response_description="Update a ingredient",
    response_model=recipes.RecipeModel,
    response_model_by_alias=False,
)
async def update_ingredient(id: str, recipe: recipes.RecipeUpdateModel):
    """
    Update individual fields of an existing recipe record.
    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    recipe = {
        k: v for k, v in recipe.model_dump(by_alias=True).items() if v is not None
    }

    if len(recipe) >= 1:
        update_result = await recipes_collection.find_one_and_update(
            {"_id": id},
            {"$set": recipe},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Recipe {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_recipe := await recipes_collection.find_one({"_id": id})) is not None:
        return existing_recipe

    raise HTTPException(status_code=404, detail=f"Recipe {id} not found")


@recipes_router.delete(root + "{id}", response_description="Recipe a ingredient")
async def delete_ingredient(id: str):
    """
    Remove a single recipe record from the database.
    """
    delete_result = await recipes_collection.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Recipe {id} not found")