import os
from os import path, environ
import random
import pickle
import string
import matplotlib.pyplot as plt 

class DataPlot:
    def __init__(self,plot, width=10, height=6):
        storage_path = path.join(environ['APPDATA'], "reporter")
        #Assure that the defauklt path exists:
        if os.path.exists(storage_path)==False:
            os.mkdir(storage_path)
        self.width = width
        self.height = height
        self.path = path.join(storage_path,generate_name()+".pkl")

        with open(self.path, 'wb') as f: 
            pickle.dump(plot, f) 
            
    def plot(self):
        with open(self.path, 'rb') as f: 
            p = pickle.load(f) 
            return p.plot(width=self.width, height=self.height)
            
    def load(self):
        with open(self.path, 'rb') as f: 
            ax = pickle.load(f) 
            return ax
        
    def create(self):
        output = ["with open(r'{}','rb') as fid:\n".format(self.path),
                  '    p = pickle.load(fid)\n',
                  f'p.plot({self.width}, {self.height})\n']
        output = "".join(i for i in output)
        return output

class DataTable:
    def __init__(self, tab):
        storage_path = path.join(environ['APPDATA'], "reporter")
        #Assure that the defauklt path exists:
        if os.path.exists(storage_path)==False:
            os.mkdir(storage_path)
        self.path = path.join(storage_path,generate_name()+".pkl")

        with open(self.path, 'wb') as f: 
            pickle.dump(tab, f) 
            
    def load(self):
        with open(self.path, 'rb') as f: 
            tab = pickle.load(f) 
            return tab
        
    def create(self):
        output = ["with open(r'{}','rb') as fid:\n".format(self.path),
                  '    p = pickle.load(fid)\n',
                  "p.style.hide(axis='index')\n"]
        output = "".join(i for i in output)
        return output

def load_report(filename):
    with open(filename, 'rb') as inp:  
        return pickle.load(inp)

def generate_name(length=10):
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for i in range(length))
    return name