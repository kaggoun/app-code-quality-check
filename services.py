import glob
import os
import sys
import line_profiler
from memory_profiler import profile
import flake8
import numpy


path = 'C:/Users/kaggoun/Desktop/DATA_CHECK_TOOLS/app-code-quality-check-main/files_uploaded/example.py'


def insert_profile(file):
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

    with open(file, "r+") as f:

        text = f.readlines()
        
        indexes=[text.index(line) for line in text if line.lstrip().startswith("def ")]
        nb_spaces=[len(line) - len(line.lstrip()) for line in text if line.lstrip().startswith("def ")]

        j=0
        for i,index in enumerate(indexes):
            text.insert(index+j, ' ' *nb_spaces[i]+"@profile")
            j=j+1
        f.truncate(0)
        f.seek(0)

        new_text=str("\n".join(text))

        f.write(new_text)
        f.close()


# file_list=["evaluate.py","test.py"]


# def insert_profile_for_many_files(file_list):
# 	for filename in file_list :
# 		insert_profile(filename)
# 		print("$$$$$$$$$$$$$$$$$$$$$$$$$$",filename)
        


def launch_flake8(file):
    os.system("flake8 " + file + " > " + file + "_flake8_output.txt")
    print('flake8 ok')


def launch_line_profiler(file):
    path = 'C:/Users/kaggoun/Desktop/DATA_CHECK_TOOLS/app-code-quality-check-main/files_uploaded/**/*.lprof'
    folder_script =[]

    os.system("kernprof -l -v " + file)

    for f in glob.glob(path, recursive=True):
            folder_script.append(f)
            #list_files.append(f.split("/")[-1])
            os.system("python -m line_profiler " + f )

    print('line_profiler ok')

def launch_memory_profiler(file):

    os.system("python -m memory_profiler " + file + " > " + file + "_memory_profiler_output.txt")
    print('memory_profiler ok')
    print('ok')



insert_profile(path)
launch_flake8(path)
launch_line_profiler(path)
launch_memory_profiler(path)
