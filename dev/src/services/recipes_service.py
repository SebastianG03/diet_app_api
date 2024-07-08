import datetime
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument
from pymongo.errors import PyMongoError
from motor.motor_asyncio import AsyncIOMotorCollection
import motor.motor_asyncio
from prediction.recommendation_system import recomendate_recipes
from prediction.user_data import UserData, get_user_data
from data.database_connection import DatabaseConnection
from models import (RecipeUpdateModel, RecipeCollection, RecipeModel)

recipes_router = APIRouter(tags=['recipes'])
#connection = DatabaseConnection()
##connection.__init__()
#recipes_collection: AsyncIOMotorCollection = connection.connect_collection(collection='recipes') 
client =motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://db_developer:dev-mongo12@daseudla.ttyxr35.mongodb.net/?retryWrites=true&w=majority&appName=DaseUdla")
db = client.get_database("dietApp")
recipes_collection = db.get_collection("recipes")

root = "/recipes/"

@recipes_router.get(
    root + 'recomendations',
    response_description="""Recomienda recetas en base a la información ingresada del usuario:
    edad en años, peso en kg, altura en cm, genero, objetivo y la cantidad de ejercicio propuesto""",
    response_model=RecipeCollection,
    response_model_by_alias=False,
    tags=["recommendations"]
)
async def list_recipes(user_data: UserData = Depends(get_user_data)):
    cursor = recipes_collection.find()
    recipes_list = await cursor.to_list(length=100)
    recipes = [RecipeModel(**recipe) for recipe in recipes_list]

    recomendated = recomendate_recipes(recipes=recipes, user_data=user_data) 
    return RecipeCollection(recipes=recomendated)



@recipes_router.post(
    root,
    response_description="Add a new recipe",
    response_model=RecipeModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_recipe(recipe: RecipeModel):
    """
    Insert a new recipe.
    A unique `id` will be created and provided in the response.
    """
    new_recipe = await recipes_collection.insert_one(
        recipe.model_dump(by_alias=True)
    )
    created_recipe = await recipes_collection.find_one(
        {"_id": new_recipe.inserted_id}
    )
    return created_recipe
@recipes_router.get(
    root,
    response_description="List all recipes",
    response_model=list[RecipeModel],
    response_model_by_alias=False,
)
async def list_recipes():
    """
    List all of the recipes data in the database.
    """
    try:
        cursor = recipes_collection.find()
        recipes_list = await cursor.to_list(length=100)
        list_recipes = []

        for recipe in recipes_list:
            list_recipes.append(recipe)

        return list_recipes
    except PyMongoError as e:
        # Manejo de errores específicos de PyMongo
        print(f"Error al acceder a la base de datos: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

    except Exception as e:
        print(f"Error inesperado: {e}")
        raise HTTPException(status_code=422, detail="Entidad no procesable")

@recipes_router.get(
    root + "{id}",
    response_description="Get a single recipe",
    response_model=RecipeModel,
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
    response_model=RecipeModel,
    response_model_by_alias=False,
)
async def update_ingredient(id: str, recipe: RecipeUpdateModel):
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