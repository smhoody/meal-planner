"""
File: meal-planner.py
Author: Steven Hoodikoff
Date: 7 May 2021
"""

from breezypythongui import EasyFrame
import tkinter
from tkinter import PhotoImage
from tkinter.font import Font

#Local
from Query import Query
from Datastore import Datastore

class Menu(EasyFrame):
    """GUI Menu for the meal planner program"""

    def __init__(self):
        """Sets up the window, list boxes, labels, text areas, and buttons"""
        EasyFrame.__init__(self, width = 800, height = 530, title = "Meal Planner")
        defaultFont = Font(family = "Bahnschrift", size = 13)
        titleFont = Font(family = "Bahnschrift", size = 20)

        self.ds = Datastore() #will retrieve ingredient names from database.json
        self.query = Query() #will hold ingredients to search for

        #Ingredient names to create list of options on GUI
        self.meats = self.ds.getMeats()
        self.vegetables = self.ds.getVeggies()
        self.spices = self.ds.getSpices()
        self.extras = self.ds.getExtras()

        
        #Vegetable options list and label
        self.vegetableLabel = self.addLabel(text = "Vegetables", row = 1, column = 0, font = defaultFont)
        self.veggieListBox = self.addListbox(row = 0, column = 0, listItemSelected = self.veggieSelected)
        for ingredient in self.vegetables:
            self.veggieListBox.insert(tkinter.END, ingredient) #add as an option in the list

        #Spice options list and label
        self.vegetableLabel = self.addLabel(text = "Spices", row = 3, column = 0, font = defaultFont)
        self.spiceListBox = self.addListbox(row = 2, column = 0, listItemSelected = self.spiceSelected)
        for ingredient in self.spices:
            self.spiceListBox.insert(tkinter.END, ingredient)
        
        #Extras options list and label
        self.vegetableLabel = self.addLabel(text = "Extras", row = 1, column = 1, font = defaultFont)
        self.extraListBox = self.addListbox(row = 0, column = 1, listItemSelected = self.extraSelected)
        for ingredient in self.extras:
            self.extraListBox.insert(tkinter.END, ingredient)
        
        #Meat options list and label
        self.vegetableLabel = self.addLabel(text = "Meats", row = 3, column = 1, font = defaultFont)
        self.meatListBox = self.addListbox(row = 2, column = 1, listItemSelected = self.meatSelected)
        for ingredient in self.meats:
            self.meatListBox.insert(tkinter.END, ingredient) 


        #Search field and label
        self.searchLabel = self.addLabel(text = "Search items", row = 1, column = 3, font = defaultFont)
        self.searchField = self.addTextArea(text = "", row = 0, column = 3, width = 10, height = 7)

        #Results list box and label
        self.searchLabel = self.addLabel(text = "Recipes", row = 3, column = 3, font = defaultFont)
        self.resultListBox = self.addListbox(row = 5, column = 3, columnspan = 2, width = 40,
                                            height = 12, listItemSelected = self.resultSelected)
        
        #Search button
        self.searchButton = self.addButton(text = "Search", row = 0, column = 2, command = self.search)

        #Clear button
        self.clearButton = self.addButton(text = "Clear", row = 1, column = 2, command = self.clear)

        #Title label
        self.titleLabel = self.addLabel(text = "MEAL PLANNER", row = 0, column = 2, font = titleFont)



    def meatSelected(self, index):
        """Update the query and search field with the selected meat"""
        self.query.update("meats", self.meatListBox.getSelectedItem())
        self.searchField.setText(self.query)
        
    def veggieSelected(self, index):
        """Update the query and search field with the selected vegetable"""
        self.query.update("vegetables", self.veggieListBox.getSelectedItem())
        self.searchField.setText(self.query)
        
    def spiceSelected(self, index):
        """Update the query and search field with the selected spice"""
        self.query.update("spices", self.spiceListBox.getSelectedItem())
        self.searchField.setText(self.query)

    def extraSelected(self, index):
        """Update the query and search field with the selected extra"""
        self.query.update("extras", self.extraListBox.getSelectedItem())
        self.searchField.setText(self.query)
    
    def resultSelected(self, index):
        """Update the query and search field with the selected extra"""
        recipes = self.ds.getRecipes() #get dictionary of recipes
        list_item = self.resultListBox.getSelectedItem() #get the name of the recipe selected

        if recipes.get(list_item, None): #search the dictionary for the recipe name
            self.messageBox(title = list_item + " recipe", message = "\n".join(recipes[list_item]))

    def search(self):
        """Search for recipes with the current ingredients in the query and display them"""
        self.resultListBox.clear() #remove previous results
        results = self.query.search() #receive list of at most 3 results
        for recipe in results: 
            self.resultListBox.insert(tkinter.END, recipe) #add recipe onto result box

    def clear(self):
        """Clear the contents of the search field and query"""
        self.query.clear()
        self.searchField.setText("")



def main():
    Menu().mainloop()

if __name__ == "__main__":
    main()