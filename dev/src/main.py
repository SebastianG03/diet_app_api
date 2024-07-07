from fastapi import FastAPI
import services.recipes_service as recipe_service
import services.ingredients_service as ingredients_service

def create_app() -> FastAPI:
    application = FastAPI()
    application.include_router(recipe_service.recipes_router)
    application.include_router(ingredients_service.ingredients_router)
    return application

app = create_app()