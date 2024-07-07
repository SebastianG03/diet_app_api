from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument
import motor.motor_asyncio
from data.database_connection import DatabaseConnection
from models import (IngredientsCollection, IngredientsModel, IngredientsUpdateModel)

ingredients_router = APIRouter(tags=['ingredients'])
#connection = DatabaseConnection()
#connection.__init__()
#ingredients_collection: AsyncIOMotorCollection = connection.connect_collection(collection='ingredients')
client =motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://db_developer:dev-mongo12@daseudla.ttyxr35.mongodb.net/?retryWrites=true&w=majority&appName=DaseUdla")
db = client.get_database("dietApp")
ingredients_collection = db.get_collection("ingredients")

root = "/ingredients/"

@ingredients_router.post(
    root,
    response_description="Add a new ingredient",
    response_model=IngredientsModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_ingredient(ingredient: IngredientsModel):
    """
    Insert a new ingredient.
    A unique `id` will be created and provided in the response.
    """
    new_ingredient = await ingredients_collection.insert_one(
        document=ingredient.model_dump(by_alias=True)
    )
    created_ingredient = await ingredients_collection.find_one(
        {"_id": new_ingredient.inserted_id}
    )
    return created_ingredient

@ingredients_router.get(
    root,
    response_description="List all ingredients",
    response_model=IngredientsCollection,
    response_model_by_alias=False,
)
async def list_ingredients():
    """
    List all of the ingredients data in the database.
    """
    ingredients = await ingredients_collection.find().to_list(100)
    return IngredientsCollection(ingredients=ingredients)

@ingredients_router.get(
    root + "{id}",
    response_description="Get a single ingredient",
    response_model=IngredientsModel,
    response_model_by_alias=False,
)
async def show_ingredient(id: str):
    """
    Get the record for a specific ingredient, looked up by `id`.
    """
    if (ingredient := await ingredients_collection.find_one({"_id": id})) is not None:
        return ingredient
    raise HTTPException(status_code=404, detail=f"Ingredient {id} not found")

@ingredients_router.get(
    root + "name/{name}",
    response_description="Get a single ingredient by name",
    response_model=IngredientsModel,
    response_model_by_alias=False,
)
async def show_ingredient_by_name(name: str):
    """
    Get the record for a specific ingredient, looked up by `name`.
    """
    if (ingredient := await ingredients_collection.find_one({"name": name})) is not None:
        return ingredient
    raise HTTPException(status_code=404, detail=f"Ingredient {name} not found")

@ingredients_router.put(
    root + "{id}",
    response_description="Update a ingredient",
    response_model=IngredientsModel,
    response_model_by_alias=False,
)
async def update_ingredient(id: str, ingredient: IngredientsUpdateModel):
    """
    Update individual fields of an existing ingredient record.
    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    ingredient = {
        k: v for k, v in ingredient.dict(by_alias=True).items() if v is not None
    }

    if len(ingredient) >= 1:
        update_result = await ingredients_collection.find_one_and_update(
            {"_id": id},
            {"$set": ingredient},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Ingredient {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_ingredient := await ingredients_collection.find_one({"_id": id})) is not None:
        return existing_ingredient

    raise HTTPException(status_code=404, detail=f"Ingredient {id} not found")

@ingredients_router.delete(root + "{id}", response_description="Delete a ingredient")
async def delete_ingredient(id: str):
    """
    Remove a single ingredient record from the database.
    """
    delete_result = await ingredients_collection.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Ingredient {id} not found")
