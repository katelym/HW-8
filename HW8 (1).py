# Your name: 
# Your student id:
# Your email:
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
from collections import OrderedDict

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """  
    

    # creating file path
    source_dir = os.path.dirname(__file__) #<-- directory name
    full_path = os.path.join(source_dir, db)
    # Create a SQL connection to our SQLite database
    con = sqlite3.connect(full_path)

    # creating cursor
    cur = con.cursor()

    # reading all table names
    cur.execute("""
        SELECT restaurants.name, categories.category, buildings.building, restaurants.rating
        FROM restaurants
        JOIN buildings ON buildings.id = restaurants.building_id
        JOIN categories ON categories.id = restaurants.category_id
        """
        )
    
    variable = cur.fetchall()
    #print(variable)
    outerdict = {}
    for x in variable:
        y = list(x)
        innerdict = {}
        #print(x)
        namev = y[0]
        #print(namev)
        genrev = y[1]
        #print(genrev)
        buildingv = y[2]
       
        ratingv = y[3]
     
        innerdict['category'] = genrev
        innerdict['building'] = buildingv
        innerdict['rating'] = ratingv
        outerdict[namev] = innerdict

    

    #fetch all --> Rarity of Fish gets everything from within the select statement
    #join statement 
    # Be sure to close the connection
    con.close()
    return outerdict 

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """

    source_dir = os.path.dirname(__file__) #<-- directory name
    full_path = os.path.join(source_dir, db)
    # Create a SQL connection to our SQLite database
    con = sqlite3.connect(db)

    # creating cursor
    cur = con.cursor()

    # reading all table names
    cur.execute("""
        SELECT categories.category, COUNT(restaurants.category_id)

        FROM restaurants
        JOIN categories ON categories.id = restaurants.category_id
        GROUP BY category
        """
        )
    
    variable = cur.fetchall()
    # con.close()
    #print(variable)
    #print(variable)
    d = dict(variable)
    sorted_dict = dict(sorted(d.items(), key = lambda t: t[1], reverse = True))
    #print(sorted_dict)
    x_var = list(sorted_dict.keys())
           
    y_var = list(sorted_dict.values())

    # #in the () x is always first if not specified 
    plt.figure(figsize = (25,8))
    plt.barh(x_var,y_var)
    plt.xlabel('Number of Restaurants') 
    plt.ylabel('Restaurant Categories')
    plt.title("Types of Restaurant on South University Ave")    
    plt.show()
    #print(sorted_dict)

    return d


def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    source_dir = os.path.dirname(__file__) #<-- directory name
    full_path = os.path.join(source_dir, db)
    # Create a SQL connection to our SQLite database
    con = sqlite3.connect(db)

    # creating cursor
    cur = con.cursor()

    # reading all table names
    cur.execute("""
        SELECT buildings.building, restaurants.name, restaurants.name 
        FROM restaurants 
        JOIN buildings ON restaurants.building_id = buildings.id WHERE buildings.building = ?""", (building_num,)
       #can take two variables first one is the sequal statement from join, where etc 
       #second argument is a tuple even if it only has one item it has to have a comma in it 
        # if i have more than one outside argument, don't need comma at the end 
        )
    
    variable = cur.fetchall()
    for x in variable: 
        print(x)

#Try calling your functions here
def main():
    # db = "South_U_Restaurants.db"
    load_rest_data("South_U_Restaurants.db")
    #plot_rest_categories("South_U_Restaurants.db")
    find_rest_in_building(1140,"South_U_Restaurants.db")
class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)
'''
    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

'''
if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
