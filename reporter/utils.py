import os
from os import path, environ
import random
import pickle
import string
import matplotlib.pyplot as plt 
import seaborn.objects as so
from typing import Union
import pandas as pd
def prep_format(
        tab:pd.DataFrame,
        int_cols: Union[None,str,list] = None,
        percent_cols: Union[None,str,list] = None,
        float_cols: Union[None,str,list] = None,
        digits = 2):
    if isinstance(percent_cols,str):
        percent_cols = [percent_cols]
    if isinstance(float_cols,str):
        float_cols = [float_cols]
    if all([col is None for col in [int_cols,percent_cols,float_cols]]):
        # default all numeric:
        format_mapping = {col: f"{{:,.{digits}f}}" for col in tab.select_dtypes(include='number').columns}
        for key, value in format_mapping.items():
            tab[key] = tab[key].apply(value.format)
    else:
        if int_cols is not None:
            tab[int_cols] = tab[int_cols].astype(int)
        if percent_cols is not None:
            format_mapping = {col: f"{{:,.{digits}%}}" for col in percent_cols}
            for key, value in format_mapping.items():
                tab[key] = tab[key].apply(value.format)
        if float_cols is not None:
            format_mapping = {col: f"{{:,.{digits}f}}" for col in float_cols}
            for key, value in format_mapping.items():
                tab[key] = tab[key].apply(value.format)
        # integers, percents und floats separat angeben 
    return tab
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
            if isinstance(p, so.Plot):
                return p.layout(size=(self.width, self.height))
            else:
                return p.plot(width=self.width, height=self.height)
            
    def load(self):
        with open(self.path, 'rb') as f: 
            ax = pickle.load(f) 
            return ax
        
    def create(self):
        output = ["with open(r'{}','rb') as fid:\n".format(self.path),
                  '    p = pickle.load(fid)\n',
                  f'p.plot()\n'] # {self.width}, {self.height}
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