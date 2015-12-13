__author__ = 'nick_toffle'
from runAPISearch import *
import time as t

# foodGroups = getFoodGroups()

# for i in foodGroups:
#     print(str(i.id)+' '+i.description)
# print('\n')
print('###########################################################################################')

def testAPI():
    groups = getFoodGroups()
    for i in groups:
        url = url_base+ntr+formatJSON+'&api_key='+key
        for j in nutList:
            url +='&nutrients='+str(j)
        url += '&fg='+str(i.id)\
               +'&max=5&offset=100'

        # insert the foods into the database
        foods = getFoodsInGroup(i, url)
        # t.sleep(2)

        # insertIntoFOODS(foods, i.id)
        for j in foods:
            print(str(j.ndbno)+': '+j.name+' | '+j.foodGroup+' | '+j.measure)

        # insert the nutrient values into the database
        allTheNuts = getNutrientsFromFood(url)
        for j in allTheNuts:
            print(str(j.id)+': '+str(j.ndbno)+' | '+j.name+' | '+j.unit+' | '+str(j.amt))

testAPI()

## testing the isinstance command:
#
# this = foodStuff(1,'yum','group',5)
# this = Nutrient(1,2,'good','SI',4.5)
# # this = FoodGroup(1,'group')
# if isinstance(this, foodStuff):
#     print('is a foodStuff')
# elif isinstance(this, Nutrient):
#     print('is a Nutrient')
# elif isinstance(this, FoodGroup):
#     print('is a food group')
