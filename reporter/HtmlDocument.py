import subprocess
import tempfile
import os
import pickle

import pandas as pd 
import shutil
import webbrowser

from .HtmlHeader import HtmlHeader
from .CodeChunk import CodeChunk
from .utils import DataPlot, DataTable

class HtmlDocument:
    def __init__(self,title="",author="",theme="default"):
        self.header = HtmlHeader(title=title,
                                 author=author,
                                 theme=theme)
        self.data = pd.DataFrame()
        self.path = None
    
    def __write_qmd(self):
        setup = CodeChunk("import matplotlib.pyplot as plt\nimport pickle\n",include=False)
        code_data = pd.concat([
            pd.DataFrame({"type":"header","name":"header","object":[self.header]}),
            pd.DataFrame({"type":"setup","name":"setup","object":[setup]}),
            self.data
        ]).reset_index()

        result = [CodeChunk(content=object.create()).create() if type in ["table","plot"] else object.create()
                  for object, type in zip(code_data.object, code_data.type) ]
        
        final_code = "".join([item for item in result])


        #path = tempfile.NamedTemporaryFile(suffix='.qmd').name
        fd, path =tempfile.mkstemp(suffix = '.qmd')
    
        with os.fdopen(fd, 'w') as tmp:
            # do stuff with temp file
            tmp.write(final_code)
            self.path = path
            
    def __render(self, rewrite_qmd = True):
        if rewrite_qmd:
            self.__write_qmd()
        process = subprocess.Popen(['quarto','render', os.path.basename(self.path)],
                                   stdin =subprocess.PIPE,
                                   stderr =subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True,
                                   cwd=os.path.dirname(self.path)) 

        self.error = ''.join(process.stderr.readlines())
        return("success")
    def __open_html(self):
        webbrowser.open(os.path.splitext(self.path)[0] + ".html")

        #print(code_data.code.str.cat(sep="\n"))
    def open(self, rewrite_qmd = True):
        if rewrite_qmd:
            self.__write_qmd()
        FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
        subprocess.run([FILEBROWSER_PATH, os.path.normpath(self.path)])
        #webbrowser.open(self.path)
    
    def print(self):
        with open(self.path, encoding="utf-8") as f:
            lines = [x for x in f]
            print(lines)
    
    def add_plot(self, plot, name,  width=8, height=4):
        dplot = DataPlot(plot, width=width, height=height)
        self.data = pd.concat([
            self.data,
            pd.DataFrame({"type":"plot","name":name,"object":[dplot]})
        ]).reset_index(drop=True)

    def add_table(self, tab, name):
        dtab = DataTable(tab)
        self.data = pd.concat([
            self.data,
            pd.DataFrame({"type":"table","name":name,"object":[dtab]})
        ]).reset_index(drop=True)

    def change_object(self,element,id=None,name=None, width=8, height=4):
        if id==None and name==None:
            raise ValueError('Please either provide an id or a plot name')
        if id!=None and (type(id) == int or type(id) == float):
            if isinstance(element, pd.DataFrame):
                self.data.at[id,'object'] = DataTable(element)
            else:
                self.data.at[id,'object'] = DataPlot(element, width=width, height=height)
       # else:
       #     self.data.at[report2.data.query("name == '{}'".format(name)).index[0],"object"] = Dataplot(ax)
        
    def render(self, rewrite_qmd = True):
        self.__render(rewrite_qmd = rewrite_qmd)
        self.__open_html()
        
    def save(self, path, rerender = True):
        extension = os.path.splitext(path)[1]
        if extension == ".html":
            if rerender:
                self.__render()
                shutil.copy2(os.path.splitext(self.path)[0] + ".html", path)
            else:
                shutil.copy2(os.path.splitext(self.path)[0] + ".html", path)
        elif extension == ".pkl":
            with open(path, 'wb') as outp:  # Overwrites any existing file.
                pickle.dump(self, outp, pickle.HIGHEST_PROTOCOL)
        else:
            raise ValueError("Path has to end with .html or .pkl")