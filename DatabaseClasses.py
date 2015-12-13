__author__ = 'nick_toffle'

# list = [id, name, foodGroup, serving, calories, fat, Cholesterol, Sodium, Potassium, Carbs, Fiber, Sugars, Protein,
#         Vit A, Vit C, Calcium, Iron, Vit D, Folic Acid, Zinc]

class foodStuff:
    def __init__(self,id,name,foodGroup,measure):
        self.ndbno = id
        self.name = name
        self.foodGroup = foodGroup
        self.measure = measure

class Nutrient:
    def __init__(self,foodID,id,name,unit,value):
        self.id = id
        self.ndbno = foodID
        self.name = name
        self.unit = unit
        self.amt = value

class FoodGroup:
    def __init__(self,id,name):
        self.id = id
        self.description = name