from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import dev.processor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


### --- Class models --- ###

class IngredientsQuery(BaseModel):
    """Data format for ingredients search"""
    ingredients: list[str]

class RecipeQuery(BaseModel):
    """Data format for recipe name"""
    name: str
    ingredients: IngredientsQuery



### --- Endpoints --- ###

@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.get("/recipe")
async def search_recipe_name(query: str) -> dict:
    """Calls MealDB api to search a recipe name"""
    response = await dev.processor.search_recipe_name(query)
    return {"response": response}

@app.post("/search-ingredients")
async def search_recipe_name(ingredients: IngredientsQuery) -> dict:
    """Calls MealDB api to search a recipe name"""
    print(ingredients)
    return {"response": ingredients}