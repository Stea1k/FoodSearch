__author__ = 'nick_toffle'

import Tkinter as tk
from switchKeys import *

class noDataWindow:
    def __init__(self,root):
        self.notice = tk.Label(root,text='Please revise your search.')
        self.notice.grid(padx=30, pady=30, row=0, column=0)

class finishedWindow:
    def __init__(self,root):
        self.notice = tk.Label(root,text='Updating Complete')
        self.notice.grid(padx=30, pady=30, row=0, column=0)