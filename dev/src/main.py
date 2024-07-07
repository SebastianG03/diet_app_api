from fastapi import FastAPI
import services.recipes_service as recipe_service
import services.ingredients_service as ingredients_service

def create_app() -> FastAPI:
    application = FastAPI()

    application.include_router(prefix="/api", tags=["recipes"], router=recipe_service.recipes_router)
    application.include_router(prefix="/api", tags=['ingredients'], router=ingredients_service.ingredients_router)
    return application

app = create_app()