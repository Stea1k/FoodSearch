__author__ = 'nick_toffle'

import sqlite3 as sql
import switchKeys as keys

# gets all measurement units.
def getUnits():
    try:
        con = sql.connect('FoodData.db')
        con.text_factory = str
        print('successful connection')
        with con:
            cur = con.cursor()
            nutUnits = []
            unitReturns = cur.execute("SELECT DISTINCT UNIT FROM NUTRIENTS")
            for i in unitReturns:
                nutUnits.append(i[0])
            return nutUnits
    except sql.Error, e:
        if con:
            con.rollback()
        print("Error %s:" % e.args[0])
    finally:
        if con:
            con.close()
            print('connection closed')
        else:
            print('connection closed')

# testing getUnits()
# for i in getUnits():
#     print(i)

# tests the database
def getAll():
    try:
        con = sql.connect('FoodData.db')
        con.text_factory = str
        print('successful connection')
        with con:
            cur = con.cursor()
            stuff = cur.execute("SELECT * FROM FOOD_GROUPS")
            print('\nthe food groups\n')
            for i in stuff.fetchall():
                print(i)

            print('\nthe foods \n')
            stuff = cur.execute("SELECT * FROM FOODS")
            for i in stuff.fetchall():
                print(i)

            print('\nthe Nutrients\n')
            stuff = cur.execute("SELECT * FROM NUTRIENTS")
            for i in stuff.fetchall():
                print(i)
    except sql.Error, e:
        if con:
            con.rollback()
        print("Error %s:" % e.args[0])
    finally:
        if con:
            con.close()
            print('connection closed')
        else:
            print('connection closed')

# getAll()

# gets all food groups from the database
def getFG():
    try:
        con = sql.connect('FoodData.db')
        con.text_factory = str
        print('successful connection')
        with con:
            cur = con.cursor()
            FGstuff = cur.execute("SELECT FOODGROUP FROM FOOD_GROUPS")
            FGlist = [i[0] for i in FGstuff.fetchall()]
            # for i in FGlist:
            #     print(str(i))
            return FGlist
    except sql.Error, e:
        if con:
            con.rollback()
        print("Error %s:" % e.args[0])
    finally:
        if con:
            con.close()
            print('connection closed')
        else:
            print('connection closed')

# gets the list of nutrient names
def getNutList():
    try:
        con = sql.connect('FoodData.db')
        con.text_factory = str
        print('successful connection')
        with con:
            cur = con.cursor()

            NUTStuff = cur.execute("SELECT DISTINCT NUTNAME FROM NUTRIENTS")
            NUTList = [i[0] for i in NUTStuff.fetchall()]
            return NUTList

    except sql.Error, e:
        if con:
            con.rollback()
        print("Error %s:" % e.args[0])
    finally:
        if con:
            con.close()
            print('connection closed')
        else:
            print('connection closed')

# returns True if a given string is equivalent to any string in a list of strings
def checkStrings(newString, listOfStrings):
    x = False
    for i in listOfStrings:
        if newString == i:
            x=True
    return x


FGlst = getFG()

# command line search testing.
def SearchTesting():
    try:
        con = sql.connect('FoodData.db')
        con.text_factory = str
        print('successful connection')
        with con:
            cur = con.cursor()

                # SELECT *
                # FROM FOODS AS F
                # JOIN NUTRIENTS AS N ON F.NDBNO = N.NDBNO

            testResult = cur.execute("""
                SELECT *
                FROM FOOD_GROUPS
                """)
            for i in testResult.fetchall():
                print(i)

    except sql.Error, e:
        if con:
            con.rollback()
        print("Error %s:" % e.args[0])
    finally:
        if con:
            con.close()
            print('connection closed')
        else:
            print('connection closed')

# SearchTesting()

# returns True if 'name' is entered
def nameCheck(name):
    if (name == 'Enter a Food' )|(name == ''):
        return False
    else: return True

# returns a reduced array based on results for each item in the array.
# eliminates unwanted values from the array.
def checkRun(strArray):
    newArray = strArray

    delArray = [i for i in newArray if (i.nutSelect.get()!="Choose")|(i.comparisonOption.get()!="range")]

    return delArray

def compareOptions(compare, nutName,val):
    sub =""
    if keys.whereSwitch == 0:
        sub+=" AND "

    sub +="NAME IN (" \
        "SELECT NAME " \
        "FROM FOODS AS F " \
        "INNER JOIN NUTRIENTS AS N ON F.NDBNO = N.NDBNO " \
        "WHERE NUTNAME LIKE '%s' AND AMT_PER_SERVING "%nutName
    if compare == 'under':
        sub += " < "
    elif compare == 'over':
        sub += " > "
    elif compare == "equal":
        sub += " = "
    sub += str(val)+") "
    keys.whereSwitch = 0
    return sub

# def setNutRangeSQL(nutArrayI):
#     newStr = ""
#
#     if keys.whereSwitch == 0:
#         newStr += " AND "
#     newStr += "(NUTNAME LIKE '"+str(nutArrayI.nutSelect.get())+"' AND"
#     keys.whereSwitch = 0
#     return newStr

# adds a 'where' to the SQL query if any of the options return 'True'.
def checkAllForSQL(category, name, nutArray):
    checkCat = checkStrings(category, FGlst)
    checkName = nameCheck(name)
    checkArray = checkRun(nutArray)
    if checkCat|checkName|(len(checkArray)>0):
        keys.whereSwitch = 1
        return " WHERE "

# adds the Food group and food name to query as needed.
def catAndName(category, name):
    checkCat = checkStrings(category, FGlst)
    checkName = nameCheck(name)

    newStr = ""

    if checkCat & checkName:
        newStr += " FOODGROUP LIKE '"+str(category)+"' AND NAME LIKE '%"+str(name)+"%'"
    elif checkCat & (not checkName):
        newStr += " FOODGROUP LIKE '"+str(category)+"'"
    elif (not checkCat) & checkName:
        newStr += " NAME LIKE '%"+str(name)+"%' "
    else:
        newStr = ""

    if checkCat |checkName:
        keys.whereSwitch = 0
    else:
        keys.whereSwitch = 1
    return newStr

# adds a subquery to the query for each comparison option.
def appendRanges(modNutArray):
    newStr = ""

    for i in modNutArray:
        # newStr += setNutRangeSQL(i)
        newStr += compareOptions(i.comparisonOption.get(), i.nutSelect.get(), i.nutRangeValue.get())

    return newStr

# runs through a large portion of the overarching options.
def addFoodNameNuts(category, name, nutArray):
    newStr = ""

    checkArray = checkRun(nutArray)

    addStr = catAndName(category, name)

    if (addStr != "")&(len(checkArray)>0):
        addStr += appendRanges(checkArray)
    elif (addStr=="")&(len(checkArray)>0):
        firstInLine = checkArray.pop(0)
        # addStr += setNutRangeSQL(firstInLine)
        addStr += compareOptions(firstInLine.comparisonOption.get(), firstInLine.nutSelect.get(), firstInLine.nutRangeValue.get())
        addStr += appendRanges(checkArray)
    print(newStr)

    newStr += addStr
    return newStr

# overarching search query.
def getBasicSearchData(category, name, nutArray):
    try:
        con = sql.connect('FoodData.db')
        con.text_factory = str
        print('successful connection\n')
        with con:
            cur = con.cursor()

            initial = """
                SELECT DISTINCT NAME,FOODGROUP,SERVING,NUTNAME,UNIT,AMT_PER_SERVING
                FROM FOODS AS F
                INNER JOIN FOOD_GROUPS AS FG ON F.GROUPID = FG.GROUPID
                INNER JOIN NUTRIENTS AS N ON F.NDBNO = N.NDBNO
                """

            try:
                initial += checkAllForSQL(category, name, nutArray)
                # print(initial+'\n')
                initial += addFoodNameNuts(category, name, nutArray)
                print(initial+'\n')
                print("'Where' and food nutrient stuff added\n")
            except:
                print(Exception)
                initial += ""

            initial += " ORDER BY FG.GROUPID"
            print(initial+'\n')

            searchResult = cur.execute(initial)
            searchResultList = [[i[0],i[1],i[2],i[3],i[4],i[5]] for i in searchResult.fetchall()]

            keys.whereSwitch = 0

            return searchResultList

    except sql.Error, e:
        if con:
            con.rollback()
        print("Error %s:" % e.args[0])
    finally:
        if con:
            con.close()
            print('connection closed')
        else:
            print('connection closed')

