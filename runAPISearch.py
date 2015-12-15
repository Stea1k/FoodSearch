__author__ = 'nick_toffle'
import requests
import json
from DatabaseClasses import *
from gitignore import *
import buildDB

# nutrient list
nutList = [203, 205, 291, 204, 324, 301, 401, 431, 303, 309, 601, 307, 306, 208, 269]

# the consolidated set of queries that grab the API data and then puts it into Dictionary format
# for later use. Usable for any dictionary acquired.
def runQ(url):
    response = requests.get(url)
    jSon = response.json()
    dumped = json.dumps(jSon)
    loaded = json.loads(dumped)
    return loaded

# pulls from a url the list of food groups
def getFoodGroups():
    # pull API database data for a list of food groups
    url = url_base+ltOption+formatJSON+'&lt=g&sort=n&api_key='+key
    # print(url)
    loaded = runQ(url)

    # use said data to create an array of Food Group objects
    listOfGroups = []
    groups = loaded['list']['item']
    # print('ran once')
    for i in groups:
        # print(i['name'],i['id'])
        newFoodGroup = FoodGroup(int(i['id']), i['name'])
        listOfGroups.append(newFoodGroup)
    return listOfGroups

# getFoodGroups()

def getNutrientsFromFood(url):
    nutrientSearchURL = url
    listOfNutrients = []
    foods = runQ(nutrientSearchURL)
    listOfFoodsFromFoods = foods['report']['foods']
    for i in listOfFoodsFromFoods:
        ndbno = int(i['ndbno'])
        nuts = i['nutrients']
        for j in nuts:
            try:
                newValue = float(j['value'])
            except:
                newValue = 0
            finally:
                newNutrient = Nutrient(int(j['nutrient_id']),ndbno,j['nutrient'],j['unit'],newValue)
                listOfNutrients.append(newNutrient)
    return listOfNutrients

# this will pull all foods for a specific food group with the given list of nutrients desired.
def getFoodsInGroup(group,url):
    foods = runQ(url)
    listOfFoods = []
    newFoods = foods['report']['foods']
    for i in newFoods:
        newFoodFromDict = foodStuff(int(i['ndbno']), i['name'],group.description, i['measure'])
        listOfFoods.append(newFoodFromDict)
    return listOfFoods

# uses both getFoodGroups and getFoodsInGroup to run through all food groups to acquire every food with all
# expected nutrients
def populateTables():
    groups = getFoodGroups()
    buildDB.insertIntoTable(groups, groups[0].id)
    print('success')
    for i in groups:
        url = url_base+ntr+formatJSON+'&api_key='+key
        for j in nutList:
            url = url+'&nutrients='+str(j)
        url += '&fg='+str(i.id)\
            +'&max=5'

        # insert the foods into the database
        foods = getFoodsInGroup(i, url)
        buildDB.insertIntoTable(foods, i.id)

        # insert the nutrient values into the database
        allTheNuts = getNutrientsFromFood(url)
        buildDB.insertIntoTable(allTheNuts, i.id)
    print('success')

# takes a dictionary and prints out all nutritional values for a specific food.
def printFoodReport(loaded):
    x = 1
    dStuff = loaded['report']['food']
    name = dStuff['name']
    nutrients = dStuff['nutrients']

    # prints the name of the food in question
    print(name+'\n')

    # prints the list of all nutrients for the given food.
    for i in nutrients:
        nValue = i['name']
        uValue = i['unit']
        vValue = float(i['value'])
        print(nValue+': '+str(vValue)+' '+uValue)
