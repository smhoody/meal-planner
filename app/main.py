from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import app.functions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### --- Class models --- ###

class recipe_name_query(BaseModel):
    """Data format for recipe name"""
    name: str

class ingredients_query(BaseModel):
    """Data format for ingredients search"""
    ingredients: list[str]



### --- Endpoints --- ###

@app.get("/v1")
async def root() -> dict:
    return {"message": "Hello World"}


@app.post("/v1/search-recipe/")
async def search_recipe_name(query: recipe_name_query) -> dict:
    """Calls MealDB api to search a recipe name"""
    print(query)
    return {"output": query}

@app.post("/v1/search-ingredients/")
async def search_recipe_name(ingredients: ingredients_query) -> dict:
    """Calls MealDB api to search a recipe name"""
    print(ingredients)
    return {"output": ingredients}