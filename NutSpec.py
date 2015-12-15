__author__ = 'nick_toffle'

from Tkinter import *
import dataSelect as dS

class nutrientSpec:
    def __init__(self,root,listOfNuts):
        root.grid_columnconfigure(0,weight=1)
        self.nutSelect = StringVar(root)
        self.nutSelect.set('Choose')
        self.comparisonOption = StringVar(root)
        self.comparisonOption.set('Range')
        self.nutRangeValue = DoubleVar(root)
        self.nutList = listOfNuts
        self.compOp = ['under','over','equal']
        # self.unitSelect = StringVar(root)
        # self.unitSelect.set('Unit')

        # Options menu
        self.options = OptionMenu(root, self.nutSelect, *self.nutList)
        self.options.grid(row=0,column=0, sticky = E+W)

        # greater/lesser/equal to options
        self.comparison = OptionMenu(root, self.comparisonOption, *self.compOp)
        self.comparison.grid(row=0, column=1, sticky = E+W)

        # value text box
        self.nutValue = Entry(root, width = 5, textvariable = self.nutRangeValue,bg="white")
        self.nutValue.grid(row=0,column=2, sticky = E+W)

        # unit options menu

        # self.unitsOptions = OptionMenu(root, self.unitSelect, *dS.getUnits())
        # self.unitsOptions.grid(row=0,column=3,sticky=E+W)

    def getNutrientSelect(self):
        return self.nutSelect.get()

    def getComparisonSelect(self):
        return self.comparisonOption.get()

    def getnutValueInput(self):
        return self.nutRangeValue.get()