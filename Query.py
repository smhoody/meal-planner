"""
File: Query.py
Author: Steven Hoodikoff
Date: 7 May 2021
"""
import json
from functools import reduce

#Local
from Datastore import Datastore

class Query():
    """Holds a dictionary of ingredients to search the datastore for"""

    def __init__(self):
        """Instantiate a database object and declare the ingredients list"""
        self.ds = Datastore()
        self.ingredients = {"meats":[], "vegetables":[], "spices":[], "extras":[]}
        self.ingredientCount = len(reduce(lambda x,y: x+y, list(self.ingredients.values())))


    def update(self, category, item):
        """Add an ingredient, unless it is already in the dictionary, then remove it
        :param category: string - for placing the ingredient in the right key
        :param item: string - ingredient for placing in the query
        """
        if not item in self.ingredients[category]: #if the ingredient is not in the search list
            self.ingredients[category].append(item) #add it
            self.ingredientCount += 1
        else: #when the item is in the list
            index = self.ingredients[category].index(item) #get the index
            self.ingredients[category].pop(index) #remove the ingredient from the list
            self.ingredientCount -= 1


    def search(self):
        """Request the datastore to search for recipes with current ingredients
        :return: list of 3 recipe names
        """
        return self.ds.search(self.ingredients.copy(), self.ingredientCount) #return top 3 matches


    def clear(self):
        """Clear all ingredients in the query"""
        for key in self.ingredients:
            self.ingredients[key].clear()
        self.ingredientCount = 0
        

    def __str__(self):
        """Return all ingredients in the query"""
        return "\n".join(reduce(lambda x,y: x+y, list(self.ingredients.values())))