__author__ = 'nick_toffle'

from Tkinter import *
from NutSpec import *
from dataSelect import *
from runAPISearch import *
from buildDB import *
import datetime
import ReportGUI
import time
import datetime as dt
import foodObject
from notification import *
import switchKeys as keys

print('success')
# root = Tk()

class ROW(Tk):
    def __init__(self, parent):
        Tk.__init__(self,parent)
        # stored nutrient requests
        self.nutSpecList = []
        self.FGlst = FGlst
        self.allNutsFromDB = getNutList()
        # stored data on the table for adding and removing temporary frames.
        self.Rows = 1
        self.range = 0
        self.column = 0
        self.reportNum = 0
        self.var1 = StringVar(parent)
        self.var1.set('Select Group')
        self.var2 = StringVar(parent)
        self.labels = []
        self.YAArray = []
        self.foodReportArray = []

        # top frame
        self.topFrame = Frame(pady=2)
        self.topFrame.grid(row=0, column=0, sticky=W+E)
        self.topFrame.grid_columnconfigure(2,weight=1)

        # dropdown list
        self.dropList = OptionMenu(self.topFrame,self.var1,'',*self.FGlst)
        self.dropList.grid(row=0, column=0,padx=2)

        # Name Entry
        self.nameLabel = Label(self.topFrame, text=' and/or ')
        self.nameLabel.grid(row=0, column=1, sticky = E+W)

        # Name text entry
        self.entry = Entry(self.topFrame, textvariable=self.var2)
        self.entry.insert(END,'Enter a Food')
        self.entry.grid(row=0, column=2, sticky = W+E)

        # Search button
        self.DBSearch = Button(self.topFrame, text='Search', command = self.searchAll)
        self.DBSearch.grid(padx=3, row=0, column=4)

        # Update Table
        self.update = Button(self.topFrame, text='Update Tables',command=self.updateDB)
        self.update.grid(padx=3,row=0,column=5)

        # bottom frame
        self.bottomFrame= Frame()
        self.bottomFrame.grid(row=1,column=0, sticky = W+E)
        self.bottomFrame.grid_columnconfigure(1,weight=1)

        # leftFrame
        self.leftFrame = Frame(self.bottomFrame)
        self.leftFrame.grid(row=0, column=0, sticky=N)

        # actionFrame
        self.actionFrame = Frame(self.leftFrame)
        self.actionFrame.grid(row=0,column=0, sticky=N+W+E)
        self.actionFrame.grid_columnconfigure(0,weight=1)

        # loweraction frame
        self.lowerActionFrame = Frame(self.leftFrame)
        self.lowerActionFrame.grid(row=1, column=0)
        self.lowerActionFrame.grid_columnconfigure(0,weight=1)

        # add/remove buttons within top frame
        Label(self.actionFrame, text='Filter by Nutrients').grid(pady = 5,row=0,column=0)

        # add/remove frame
        self.addRemoveFrame = Frame(self.actionFrame)
        self.addRemoveFrame.grid(row=1,column=0,sticky = W+E)
        self.addRemoveFrame.grid_columnconfigure(0,weight=1)
        self.addRemoveFrame.grid_columnconfigure(1,weight=1)

        # add button
        self.addButton = Button(self.addRemoveFrame, text='new range', command=self.add, width=8)
        self.addButton.grid(padx=0, pady=0, row=1, column=0, sticky=W+E)

        # remove button
        self.removeButton = Button(self.addRemoveFrame, text='remove last',command=self.remove, width = 8)
        self.removeButton.grid(padx=0, pady=0, row=1, column=1, sticky=W+E)

        # output frame
        self.outputFrame = Frame(self.bottomFrame)
        self.outputFrame.grid(padx = 4,row=0,column=1, sticky=W+E+N+S)
        self.outputFrame.grid_columnconfigure(0,weight=1)
        self.outputFrame.grid_rowconfigure(1,weight=1)

        # listLabel
        self.outputLabel = Label(self.outputFrame, text='Data Output')
        self.outputLabel.grid(pady = 5,row=0,column=0)

        # listbox within bottom frame
        self.listed = Listbox(self.outputFrame)
        self.listed.insert(END, 'start')
        self.listed.grid(padx=2,pady=2,row=1,column=0, sticky=W+E+N+S)
        self.listed.config(height = 10, width = 90)

        # FooterFrame
        # self.footerFrame = Frame(self.outputFrame)
        # self.footerFrame.grid(padx=2, row=2, column=0)

        # Table switch
        # self.switchButton = Button(self.footerFrame, text = 'Change Data')
        # self.switchButton.grid(row =0, column=0, sticky=E+W)

        # Save button
        # self.saveData = Button(self.footerFrame, text = 'Save', command = self.saveFoodItem())
        # self.saveData.grid(row=0, column=1, padx=2, sticky = W+E)

        # Print Report
        # self.printReport = Button(self.footerFrame, text = 'Request Report',command = self.submitReport)
        # self.printReport.grid(row=0, column=2, padx=2, sticky=E+W)

        # sets 1 nutrient range option by default
        self.add()

    def searchAll(self):
        self.listed.delete(0, END)
        # for i in self.YAArray:
        #     print(i.nutSelect.get())
        searchResultList = getBasicSearchData(self.var1.get(), self.var2.get(), self.YAArray)
        if len(searchResultList)<1:
            keys.notificationSwitch = 'No Data'
            print(keys.notificationSwitch)
            self.notifyUser()

        else:
            for i in searchResultList:
                insertion = ''
                for j in i:
                    insertion += str(j)+' | '
                self.listed.insert(END,insertion)

        # self.nutFramesTesting()

    def remove(self):
        if(self.Rows > (self.range+1)):
            self.Rows = self.Rows - 1
            self.labels[-1].destroy()
            del self.labels[-1]
            del self.YAArray[-1]

    def appendTolisted(self,listOfData):
        for i in listOfData:
            self.listed.insert(END, i)

    def add(self):
        self.Rows +=1

        # new Frame for Nutrient options
        mainNutFrame = Frame(self.lowerActionFrame)
        self.labels.append(mainNutFrame)
        self.labels[-1].grid(padx=0, pady=0, row=self.Rows, column=0, sticky=W+E)

        # lower Frame within mainNutFrame
        self.lowerNutFrame = nutrientSpec(self.labels[-1], self.allNutsFromDB)

        # save the data inside an array?
        self.YAArray.append(self.lowerNutFrame)

    def nutFramesTesting(self):
        for i in self.YAArray:
            print(i.nutSelect.get())

    def updateDB(self):
        DBConstructor()
        populateTables()
        keys.notificationSwitch = 'finished'
        self.notifyUser()

    def notifyUser(self):
        t = Toplevel()
        t.wm_title('Notice')
        if notificationSwitch == 'No Data':
            noDataWindow(t)
        elif notificationSwitch == 'finished':
            finishedWindow(t)

if __name__ == "__main__":
    window = ROW(None)
    window.mainloop()

# ROW(root)
# root.mainloop()