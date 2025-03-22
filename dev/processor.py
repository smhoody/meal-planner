import httpx

MEALDB_BASE_URL = "https://www.themealdb.com/api/json/v1/1"
SEARCH_URL = "/search.php?s="

async def search_recipe_name(name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MEALDB_BASE_URL}{SEARCH_URL}{name}")
        return response.json()
    