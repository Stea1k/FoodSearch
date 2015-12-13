__author__ = 'nick_toffle'

import Tkinter as tk
import time
import datetime as dt

class Report():
    def __init__(self,root,num):

        # base frame for report
        self.base = tk.Frame(root)
        self.base.pack()

        # top Frame
        self.topFrame = tk.Frame(self.base)
        self.topFrame.pack(side="top")

        # report name
        self.reportName = tk.Label(self.topFrame,text='Food Report %s' % str(num))
        self.reportName.grid(row=0,column=0)

        # bottom Frame
        self.bottomFrame = tk.Frame(self.base)
        self.bottomFrame.pack(side="bottom")

        # list box
        self.reportBox = tk.Listbox(self.bottomFrame,width=100)

