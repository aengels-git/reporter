import subprocess
import tempfile
import os
import pickle

import pandas as pd 
import shutil
import webbrowser
import threading

from .PDFHeader import PDFHeader
from .CodeChunk import CodeChunk
from .utils import DataPlot, DataTable
from .TextChunk import TextChunk
class PDFDocument:
    def __init__(self,title="",author=""):
        self.header = PDFHeader(title=title,
                                author=author)
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
        subprocess.Popen(['quarto','render', os.path.basename(self.path)],
                                   stdin =subprocess.PIPE,
                                   stderr =subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True,
                                   shell=True,
                                   cwd=os.path.dirname(self.path)) 
        return("success")
    
    def __open_pdf(self):
        webbrowser.open(os.path.splitext(self.path)[0] + ".pdf")

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

    def add_table(self, tab:pd.DataFrame, name:str):
        dtab = DataTable(tab)
        self.data = pd.concat([
            self.data,
            pd.DataFrame({"type":"table","name":name,"object":[dtab]})
        ]).reset_index(drop=True)

    def text(self, content:str, level:int=0):
        self.data = pd.concat([
            self.data,
            pd.DataFrame({"type":"text","name":"text","object":[TextChunk(content=content, level=level)]})
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
 
        if rewrite_qmd:
            self.__write_qmd()

        def bg_render(document):
            process = subprocess.Popen(['quarto','render', os.path.basename(document.path)],
                            stdin =subprocess.PIPE,
                            stderr =subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            universal_newlines=True,
                            shell=True,
                            cwd=os.path.dirname(document.path))  
            print(''.join(process.stdout.readlines()))
            print(''.join(process.stderr.readlines()))
            process.wait()
            document.__open_html()
        x = threading.Thread(target=bg_render, args=(self,))
        x.start()

    def save(self, path):
        extension = os.path.splitext(path)[1]
        if extension == ".pdf":
            self.__write_qmd()
            def bg_save_html(document, path):
                process = subprocess.Popen(['quarto','render', os.path.basename(document.path)],
                                stdin =subprocess.PIPE,
                                stderr =subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                universal_newlines=True,
                                shell=True,
                                cwd=os.path.dirname(document.path))  
                print(''.join(process.stdout.readlines()))
                print(''.join(process.stderr.readlines()))
                process.wait()
                shutil.copy2(os.path.splitext(document.path)[0] + ".pdf", path)

            x = threading.Thread(target=bg_save_html, kwargs={'document': self,'path': path})
            x.start()
        elif extension == ".pkl":
            with open(path, 'wb') as outp:  # Overwrites any existing file.
                pickle.dump(self, outp, pickle.HIGHEST_PROTOCOL)
        else:
            raise ValueError("Path has to end with .html or .pkl")