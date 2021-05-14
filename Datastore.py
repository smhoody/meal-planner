"""
File: Datastore.py
Author: Steven Hoodikoff
Date: 7 May 2021
"""
import json
import pymongo
from pymongo import MongoClient
from functools import reduce

class Datastore():
    """Accesses the database, holds ingredients and recipes, and performs searches"""

    def __init__(self):
        """Instantiate with recipes and ingredients"""
        self._database = self.__getDatabase()
        self._ingredients = self._database["ingredients"] #from ingredients collection
        
        self._meats = self._ingredients.find_one({"_id":"Meats"})["ingredients"]
        self._vegetables = self._ingredients.find_one({"_id":"Vegetables"})["ingredients"]
        self._spices = self._ingredients.find_one({"_id":"Spices"})["ingredients"]
        self._extras = self._ingredients.find_one({"_id":"Extras"})["ingredients"]

        self._recipes = {}
        #change recipe format to {"name":"ingredients"}
        for recipe in self._database["recipes"].find({}): #from recipes collection
            self._recipes[recipe.get("_id")] = recipe.get("ingredients", None)

    #Accessors
    def getRecipes(self):
        """Get dictionary of recipes"""
        return self._recipes
    
    def getMeats(self):
        """Get list of meats"""
        return self._meats
    
    def getVeggies(self):
        """Get list of vegetables"""
        return self._vegetables

    def getSpices(self):
        """Get list of spices"""
        return self._spices
    
    def getExtras(self):
        """Get list of extra ingredients"""
        return self._extras


    def search(self, ingredients, ingredientCount):
        """Search the recipes with current ingredients
        :param ingredients: dict - ingredients in the query
        :param ingredientCount: int - number of ingredients in the query
        :return: list - 3 recipes that best match the search
        """
        matchIndex = 0
        recipeNames, recipeScores = [], []
        results = []

        if ingredientCount > 0:
            for recipeName, recipe in self._recipes.items():
                #Check if any meat matches between the query and recipe
                containsMeat = self.__checkMeat(ingredients["meats"], recipe)

                #Check how many matches in the ingredients between query and recipe
                matches, missing = self.__checkIngredients(ingredients, recipe)
                
                #Get the rating of how similar the ingredients are in the query and recipe
                matchIndex = self.__getIndexScore(matches, missing, containsMeat, ingredientCount)
                
                if matchIndex > 0:
                    #Add the recipe to the sorted list
                    recipeNames, recipeScores = self.__addRecipe(matchIndex, recipeName, 
                                                                recipeNames, recipeScores)               
            
            results = recipeNames.copy() #save the top 3 matches
        else:
            results = self._recipes.keys() #display recipe names when search is empty

        if len(results) == 0: #if no recipes were a match
            results = ["No recipes found with that query"]
        
        return results #return top 3 matches
    

    #Private methods
    def __checkIngredients(self, ingredients, recipe):
        """Check each ingredient in the recipe with the ingredients in the query
        :param ingredients: dict - ingredients in the query
        :param recipe: list - ingredients in the recipe
        :return matches: int - number of matching ingredients between query and recipe
        :return missing: int - number of missing ingredients between query and recipe
        """
        matches = missing = 0
        ingredientList = reduce(lambda x,y: x+y, list(ingredients.values())) #combine all ingredients in query
        ingredientCount = len(ingredientList)

        #Traverse through the ingredients in the query and check if they're in the recipe
        for ingredient in ingredientList:
            if ingredient in recipe:
                matches += 1
            else:
                missing += 1
        
        #If the recipe has more ingredients than the query, they count as missing in the query 
        if len(recipe) > ingredientCount:
            missing += len(recipe) - ingredientCount

        return matches, missing

    def __checkMeat(self, meatList, recipe):
        """Check if the recipe contains the same meat as in the query
        :param meatList: list - list of meat in the query
        :param recipe: list - list of ingredients in the recipe
        :return: boolean
        """
        match = False
        for meat in meatList:
            if meat in recipe:
                match = True
        
        return match

    def __getIndexScore(self, matches, missing, containsMeat, ingredientCount):
        """Rate the similarity of the recipe compared to the ingredients
        :param matches: int - number of matches between query and recipe
        :param missing: int - number of missing ingredients between query and recipe
        :param containsMeat: boolean - whether the meat in query is in the recipe
        :param ingredientCount: int - number of ingredients in query
        :return: int
        """
        POSITIVE_WEIGHT = 2
        NEGATIVE_WEIGHT = 10

        positiveIndex = matches / ingredientCount
        negativeIndex = missing / ingredientCount
        if containsMeat: positiveIndex *= POSITIVE_WEIGHT
        
        return (positiveIndex - (negativeIndex / NEGATIVE_WEIGHT))

    def __addRecipe(self, matchIndex, recipe, recipeNames, recipeScores):
        """Add the recipe to possible recipes in order from highest match to lowest match
        :param matchIndex: int - rating of the recipe
        :param recipe: string - name of the recipe
        :param recipeNames: list - recipe names that will be in results
        :param recipeScores: list - recipe scores that will be in results
        :return recipeNames: list
        :return recipeScores: list
        """
        index = 0
        sorted = False

        while not sorted and index < len(recipeScores):
            if matchIndex > recipeScores[index]: #if the recipe score is higher than one stored
                #add the recipe into the lists
                recipeScores.insert(index, matchIndex)
                recipeNames.insert(index, recipe)
                
                #remove the 3rd recipe
                recipeScores.pop()
                recipeNames.pop()
                sorted = True
            index += 1
        
        if not sorted and len(recipeScores) < 3: #if the recipe score was not higher than any recipe in the list, add to the end
            recipeScores.append(matchIndex)
            recipeNames.append(recipe)

        return recipeNames, recipeScores
    

    def __getDatabase(self):
        """Retrieve collections from MealPlanner database on MongoDB
        :return: dict
        """
        with open("content\\DB_string.txt", 'r') as f:
            connect_string = f.readline().strip()

        cluster = MongoClient(connect_string)
        
        return cluster["MealPlanner"]