from fastapi import FastAPI
import services.recipes_service as recipe_service 

def create_app() -> FastAPI:
    application = FastAPI()

    application.include_router(prefix="/api", tags=["recipes"], router=recipe_service.recipes_router)
    return application

app = create_app()