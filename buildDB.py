__author__ = 'nick_toffle'
import sqlite3 as sql
import sys
from runAPISearch import *
from DatabaseClasses import *

foodGroupURL = 'http://api.nal.usda.gov/ndb/list?format=json&lt=g&sort=n&api_key='
# list = [id, name, foodGroup, serving, calories, fat, Cholesterol, Sodium, Potassium, Carbs, Fiber, Sugars, Protein,
#         Vit A, Vit C, Calcium, Iron, Vit D, Folic Acid, Zinc]

# http://api.nal.usda.gov/ndb/nutrients/?format=json&api_key=DEMO_KEY&offset=0&nutrients=203&nutrients=205&nutrients=204&nutrients=208&nutrients=269&nutrients=291&nutrients=324&nutrients=301&nutrients=401&nutrients=431&nutrients=303&nutrients=309&nutrients=601&nutrients=307&nutrients=306
# needs to be capable of pagin through multiple food, unless using subset.
# http://api.nal.usda.gov/ndb/nutrients/?format=json&api_key=DEMO_KEY&offset=0&subset=1&max=1000&nutrients=203&nutrients=205&nutrients=204&nutrients=208&nutrients=269&nutrients=291&nutrients=324&nutrients=301&nutrients=401&nutrients=431&nutrients=303&nutrients=309&nutrients=601&nutrients=307&nutrients=306

# creates the FoodData database with tables
def DBConstructor():
    try:

        con = sql.connect('FoodData.db')
        print('successful connection')
        with con:

            cur = con.cursor()
            cur.executescript("""
                    DROP TABLE IF EXISTS FOOD_GROUPS;
                    CREATE TABLE FOOD_GROUPS(
                    GROUPID INT NOT NULL PRIMARY KEY,
                    FOODGROUP TEXT);
                    """)
            cur.executescript("""
                    DROP TABLE IF EXISTS FOODS;
                    CREATE TABLE FOODS(
                    NDBNO INT NOT NULL,
                    NAME TEXT NOT NULL,
                    GROUPID INT NOT NULL,
                    SERVING TEXT NOT NULL)
                    """)
            cur.executescript("""
                    DROP TABLE IF EXISTS NUTRIENTS;
                    CREATE TABLE NUTRIENTS(
                    NDBNO INT NOT NULL,
                    NUTID INT NOT NULL,
                    NUTNAME TEXT,
                    UNIT TEXT,
                    AMT_PER_SERVING REAL);
                    """)

        con.commit()
        print('Database Built Sucessfully.')
    except sql.Error, e:
        if con:
            con.rollback()

        print("Error %s:" % e.args[0])
        sys.exit(1)

    finally:
        if con:
            con.close()

# def updateSaved(foodname, addDrop):
#     try:
#         con = sql.connect('FoodData.db')
#         print('successful connection')
#         with con:
#             cur = con.cursor()
#
#             try:
#                 update = cur.execute("UPDATE FOODS SET FOODSAVED = "+str(addDrop)+" WHERE NAME = "+str(foodname))
#                 print('Update successful')
#             except:
#                 print("Unable to make requested update.")
#
#     except sql.Error, e:
#         print("Error %s:" % e.args[0])
#         sys.exit(1)
#     finally:
#         if con:
#             con.close()
#             print('connection closed')
#         else:
#             print('connection closed')

def insertIntoTable(objectList,group):
    try:
        con = sql.connect('FoodData.db')
        print('successful connection')
        with con:
            cur = con.cursor()
            try:
                firstOfLine = objectList[0]
                if isinstance(firstOfLine,FoodGroup):
                    for i in objectList:
                        foodGroupStuff = [i.id,i.description]
                        cur.execute("""INSERT INTO FOOD_GROUPS VALUES(?,?)""", foodGroupStuff)
                    print('success!')
                elif isinstance(firstOfLine,foodStuff):
                    for i in objectList:
                        newfood = [i.ndbno,i.name,group,i.measure]
                        cur.execute("""INSERT INTO FOODS VALUES (?,?,?,?);""", newfood)
                    print('success')
                elif isinstance(firstOfLine,Nutrient):
                    for i in objectList:
                        newNutrientStuff = [i.id,i.ndbno,i.name,i.unit,i.amt]
                        cur.execute("""INSERT INTO NUTRIENTS VALUES(?,?,?,?,?)""", newNutrientStuff)
                    print('success')
                con.commit()
            except sql.Error, e:
                if con:
                    con.rollback()
                print("Error %s:" % e.args[0])
                sys.exit(1)
    except sql.Error, e:
        print("Error %s:" % e.args[0])
        sys.exit(1)
    finally:
        if con:
            con.close()
            print('connection closed')
        else:
            print('connection closed')
