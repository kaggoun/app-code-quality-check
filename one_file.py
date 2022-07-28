import cProfile
import glob
import os
import sys
import re
import inspect
import ast
from inspect import getfullargspec
import line_profiler
import memory_profiler
import gprof2dot
import flake8


path = '/home/kevin/PycharmProjects/Codes_Quality_Check/test2.py'
def collect_files(path):
    """
       collect all .py files from specified path
       Parameters
       ----------
       path: string
       path to python files
       Return
       ----------       list_files: list
       list containing all names of python files
    """
    folder_script = []
    list_files = []

    for f in glob.glob(path, recursive=True):
        if "main" not in f:
            folder_script.append(f)
            list_files.append(f.split("/")[-1])

    return folder_script

print(collect_files(path))
data = collect_files(path)


def insert_def(data):
    """
       Insertion of "@Profile" if a python script contains a function

       Parameters
       ----------
       data:list
       path to python files

       Return
       ----------
       Write on each python script "@Profile"

    """
    all_function=[]
    index_function=[]

    for filename in data:
        #print(filename)
        with open(filename, "r") as f:
            text = f.readlines()
            #print(text.split("\n"))



            #p = ast.parse(text)
            #print(len(text))
            #all_function = [node.name for node in ast.walk(p) if isinstance(node, ast.FunctionDef)]
            for i in range(0, len(text)):
                if text[i].startswith("def "):
                    all_function.append(text[i])

                    index_function.append(i)



            new_list = [s.replace("def", "") for s in all_function]
            new_list = [s.replace(":", "") for s in new_list]



            for j in range(0, len(new_list)):

                    list_index_def_2 = [idx-1 for idx, j in enumerate(text) if "def" in j]

                    text.insert(list_index_def_2[j], "@profile")
                    print(text.insert(len(text), new_list[j][1:]))

                    #text.insert(list_index_def_2[j].split(","),"@profile")

            print(type(new_list))
        with open(filename, "w") as f:
           text = "".join(text)
           f.write(text)



def launch_flake8(file):
    os.system("flake8 " + file + " > " + file + "_flake8_output.txt")
    print('flake8 ok')

def launch_line_profiler(file):
    path = '/home/kevin/PycharmProjects/Codes_Quality_Check/**/*.lprof'
    folder_script =[]

    os.system("kernprof -l -v " + file)

    for f in glob.glob(path, recursive=True):
            folder_script.append(f)
            #list_files.append(f.split("/")[-1])
            os.system("python -m line_profiler " + f )

    print('line_profiler ok')

def launch_memory_profiler(file):
    os.system("python -m memory_profiler " + file)
    print('memory_profiler ok')


def launch_grof2dot(file):
    path = '/home/kevin/PycharmProjects/Codes_Quality_Check/**/*.pstats'

    folder_script = []

    os.system("python -m cProfile -o test.pstats "+ file)

    for f in glob.glob(path, recursive=True):
        folder_script.append(f)
        # list_files.append(f.split("/")[-1])
        #print(folder_script)
        #os.system("python -m line_profiler " + f)
        os.system("gprof2dot -f pstats " + f + " | dot -Tpdf -o test.pdf")
    print('gprof2dot ok')

collect_files(path)
data = collect_files(path)
insert_def(data)
launch_flake8(path)
launch_line_profiler(path)
launch_memory_profiler(path)
launch_grof2dot(path)
