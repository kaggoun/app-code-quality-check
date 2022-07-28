import sys
import re
import cProfile
import inspect
import ast
from inspect import getfullargspec
import line_profiler
import memory_profiler
import gprof2dot
import flake8
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image
import glob
import os
import streamlit as st
import streamlit.components.v1 as components
import services
import base64
import os
import json
import pickle
import uuid
import re




def main():
    def _max_width_():
        max_width_str = f"max-width: 1000px;"
        st.markdown(
            f"""
        <style>
        .reportview-container .main .block-container{{
            {max_width_str}
        }}
        </style>
        """,
            unsafe_allow_html=True,
        )

    # Hide the Streamlit header and footer
    def hide_header_footer():
        hide_streamlit_style = """
                    <style>
                    footer {visibility: hidden;}
                    </style>
                    """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # increases the width of the text and tables/figures
    _max_width_()

    # hide the footer
    hide_header_footer()

    images = Image.open('images/hi-paris-lancement-ecole-polytechnique-x.png')
    st.image(images, width=200, caption="Image 'Hi! PARIS' Research Center.")

    st.markdown("# Code Quality Check 🔍 ✅")
    st.markdown("### Check the basic quality of any code and generate  reports 🧐")
    st.markdown("     ")




    st.sidebar.header("Dashboard")
    st.sidebar.markdown("---")

    st.sidebar.header("Upload ZIP or Python File")
    uploaded_files = st.sidebar.file_uploader("", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        st.write(bytes_data)
        #insert_profile(uploaded_file)

    st.sidebar.markdown("---")
    st.sidebar.header("Select Process to Run")
    steps_process = st.sidebar.selectbox('', ['01 - Code Quality', '02 - Code Execution Time',
                                          '03 - Code Memory Optimization'])
                                          
    st.sidebar.header("Select Script Uploaded")
    steps_script = st.sidebar.selectbox('', uploaded_files)
    st.sidebar.header("Select Function in Script")

    steps_function = st.sidebar.selectbox('', ['function1', 'function2'])
    st.sidebar.markdown("---")
    st.sidebar.markdown(" ")
    st.sidebar.markdown(" ")
    st.sidebar.button('Run Process')
    st.markdown("---")

    st.markdown(f"## Output of '{steps_process}' :")

    if steps_process == "01 - Code Quality":
        os.system("flake8 " + "test2.py" + " > " + "test2" + "_flake8_output.txt")
        with open ("test2_flake8_output.txt", "r") as myfile:
             data = myfile.read().splitlines()
             for i in range(0,len(data)):
                 st.warning(data[i])

        def download_button(object_to_download, download_filename, button_text, pickle_it=False):
            """
            Generates a link to download the given object_to_download.
            Params:
            ------
            object_to_download:  The object to be downloaded.
            download_filename (str): filename and extension of file. e.g. mydata.csv,
            some_txt_output.txt download_link_text (str): Text to display for download
            link.
            button_text (str): Text to display on download button (e.g. 'click here to download file')
            pickle_it (bool): If True, pickle file.
            Returns:
            -------
            (str): the anchor tag to download object_to_download
            Examples:
            --------
            download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
            download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')
            """
            if pickle_it:
                try:
                    object_to_download = pickle.dumps(object_to_download)
                except pickle.PicklingError as e:
                    st.write(e)
                    return None

            else:
                if isinstance(object_to_download, bytes):
                    pass

                elif isinstance(object_to_download, pd.DataFrame):
                    object_to_download = object_to_download.to_csv(index=False)

                # Try JSON encode for everything else
                else:
                    object_to_download = json.dumps(object_to_download)

            try:
                # some strings <-> bytes conversions necessary here
                b64 = base64.b64encode(object_to_download.encode()).decode()

            except AttributeError as e:
                b64 = base64.b64encode(object_to_download).decode()

            button_uuid = str(uuid.uuid4()).replace('-', '')
            button_id = re.sub('\d+', '', button_uuid)

            custom_css = f""" 
                <style>
                    #{button_id} {{
                        background-color: rgb(255, 255, 255);
                        color: rgb(38, 39, 48);
                        padding: 0.25em 0.38em;
                        position: relative;
                        text-decoration: none;
                        border-radius: 4px;
                        border-width: 1px;
                        border-style: solid;
                        border-color: rgb(230, 234, 241);
                        border-image: initial;
                    }} 
                    #{button_id}:hover {{
                        border-color: rgb(246, 51, 102);
                        color: rgb(246, 51, 102);
                    }}
                    #{button_id}:active {{
                        box-shadow: none;
                        background-color: rgb(246, 51, 102);
                        color: white;
                        }}
                </style> """

            dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'

            return dl_link

        #def file_selector(folder_path='.'):
        #    filenames = os.listdir(folder_path)
        #    selected_filename = st.selectbox('Select a file', filenames)
        #    return os.path.join(folder_path, selected_filename)

        if __name__ == '__main__':


            # ---------------------
            # Download from memory
            # ---------------------

            # --------------------------
            # Select a file to download
            # --------------------------

            #st.write('~> Use if you want to test uploading / downloading a certain file.')

            # Upload file for testing
            #folder_path = st.text_input('Enter directory: deafult .', '.')
            #filename = file_selector(folder_path=folder_path)

            # Load selected file
            with open("test2_flake8_output.txt", 'rb') as f:
                s = f.read()

            download_button_str = download_button(s, "test2_flake8_output.txt",
                                                      'Download: 01 Code Quality - test2 - function1 - output')
            st.markdown(download_button_str, unsafe_allow_html=True)

    if steps_process == "02 - Code Execution Time":

        os.system("kernprof -l -v " + "test3.py")
        os.system("python -m line_profiler " + "test3.py.lprof > test2_line_profiler_output.txt")

        with open ("test2_line_profiler_output.txt", "r") as myfile:
             data2 = myfile.read().splitlines()

        #contents = open("test2_line_profiler_output.txt", "r")
        #with open("test2_line_profiler_output.html", "w") as e:
        #    for lines in contents.readlines():
        #        e.write("<pre>" + lines + "</pre> <br>\n")

        images = Image.open('images/line-profiler.png')
        st.image(images, width=800)

        def download_button(object_to_download, download_filename, button_text, pickle_it=False):
            """
            Generates a link to download the given object_to_download.
            Params:
            ------
            object_to_download:  The object to be downloaded.
            download_filename (str): filename and extension of file. e.g. mydata.csv,
            some_txt_output.txt download_link_text (str): Text to display for download
            link.
            button_text (str): Text to display on download button (e.g. 'click here to download file')
            pickle_it (bool): If True, pickle file.
            Returns:
            -------
            (str): the anchor tag to download object_to_download
            Examples:
            --------
            download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
            download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')
            """
            if pickle_it:
                try:
                    object_to_download = pickle.dumps(object_to_download)
                except pickle.PicklingError as e:
                    st.write(e)
                    return None

            else:
                if isinstance(object_to_download, bytes):
                    pass

                elif isinstance(object_to_download, pd.DataFrame):
                    object_to_download = object_to_download.to_csv(index=False)

                # Try JSON encode for everything else
                else:
                    object_to_download = json.dumps(object_to_download)

            try:
                # some strings <-> bytes conversions necessary here
                b64 = base64.b64encode(object_to_download.encode()).decode()

            except AttributeError as e:
                b64 = base64.b64encode(object_to_download).decode()

            button_uuid = str(uuid.uuid4()).replace('-', '')
            button_id = re.sub('\d+', '', button_uuid)

            custom_css = f""" 
                <style>
                    #{button_id} {{
                        background-color: rgb(255, 255, 255);
                        color: rgb(38, 39, 48);
                        padding: 0.25em 0.38em;
                        position: relative;
                        text-decoration: none;
                        border-radius: 4px;
                        border-width: 1px;
                        border-style: solid;
                        border-color: rgb(230, 234, 241);
                        border-image: initial;
                    }} 
                    #{button_id}:hover {{
                        border-color: rgb(246, 51, 102);
                        color: rgb(246, 51, 102);
                    }}
                    #{button_id}:active {{
                        box-shadow: none;
                        background-color: rgb(246, 51, 102);
                        color: white;
                        }}
                </style> """

            dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'

            return dl_link

        #def file_selector(folder_path='.'):
        #    filenames = os.listdir(folder_path)
        #    selected_filename = st.selectbox('Select a file', filenames)
        #    return os.path.join(folder_path, selected_filename)

        if __name__ == '__main__':


            # ---------------------
            # Download from memory
            # ---------------------

            # --------------------------
            # Select a file to download
            # --------------------------

            #st.write('~> Use if you want to test uploading / downloading a certain file.')

            # Upload file for testing
            #folder_path = st.text_input('Enter directory: deafult .', '.')
            #filename = file_selector(folder_path=folder_path)

            # Load selected file
            with open("test2_line_profiler_output.txt", 'rb') as f:
                s = f.read()

            download_button_str = download_button(s, "test2_line_profiler_output.txt",
                                                      'Download: 02 Code Execution Time - test2 function1 & 2 - output')
            st.markdown(download_button_str, unsafe_allow_html=True)

    if steps_process == "03 - Code Memory Optimization":
        os.system("python -m memory_profiler " + "test4.py")

        images = Image.open('images/memory-profiler.png')
        st.image(images, width=800)

        #with open ("test2_line_profiler_output.txt", "r") as myfile:
        #     data2 = myfile.read().splitlines()
        def download_button(object_to_download, download_filename, button_text, pickle_it=False):
            """
            Generates a link to download the given object_to_download.
            Params:
            ------
            object_to_download:  The object to be downloaded.
            download_filename (str): filename and extension of file. e.g. mydata.csv,
            some_txt_output.txt download_link_text (str): Text to display for download
            link.
            button_text (str): Text to display on download button (e.g. 'click here to download file')
            pickle_it (bool): If True, pickle file.
            Returns:
            -------
            (str): the anchor tag to download object_to_download
            Examples:
            --------
            download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
            download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')
            """
            if pickle_it:
                try:
                    object_to_download = pickle.dumps(object_to_download)
                except pickle.PicklingError as e:
                    st.write(e)
                    return None

            else:
                if isinstance(object_to_download, bytes):
                    pass

                elif isinstance(object_to_download, pd.DataFrame):
                    object_to_download = object_to_download.to_csv(index=False)

                # Try JSON encode for everything else
                else:
                    object_to_download = json.dumps(object_to_download)

            try:
                # some strings <-> bytes conversions necessary here
                b64 = base64.b64encode(object_to_download.encode()).decode()

            except AttributeError as e:
                b64 = base64.b64encode(object_to_download).decode()

            button_uuid = str(uuid.uuid4()).replace('-', '')
            button_id = re.sub('\d+', '', button_uuid)

            custom_css = f""" 
                <style>
                    #{button_id} {{
                        background-color: rgb(255, 255, 255);
                        color: rgb(38, 39, 48);
                        padding: 0.25em 0.38em;
                        position: relative;
                        text-decoration: none;
                        border-radius: 4px;
                        border-width: 1px;
                        border-style: solid;
                        border-color: rgb(230, 234, 241);
                        border-image: initial;
                    }} 
                    #{button_id}:hover {{
                        border-color: rgb(246, 51, 102);
                        color: rgb(246, 51, 102);
                    }}
                    #{button_id}:active {{
                        box-shadow: none;
                        background-color: rgb(246, 51, 102);
                        color: white;
                        }}
                </style> """

            dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'

            return dl_link

        #def file_selector(folder_path='.'):
        #    filenames = os.listdir(folder_path)
        #    selected_filename = st.selectbox('Select a file', filenames)
        #    return os.path.join(folder_path, selected_filename)

        if __name__ == '__main__':


            # ---------------------
            # Download from memory
            # ---------------------

            # --------------------------
            # Select a file to download
            # --------------------------

            #st.write('~> Use if you want to test uploading / downloading a certain file.')

            # Upload file for testing
            #folder_path = st.text_input('Enter directory: deafult .', '.')
            #filename = file_selector(folder_path=folder_path)

            # Load selected file
            with open("yo.txt", 'rb') as f:
                s = f.read()

            download_button_str = download_button(s, "yo.txt",
                                                      'Download: 03 Code Memory Optimization - test2 function 1 & 2 - output')
            st.markdown(download_button_str, unsafe_allow_html=True)

if __name__ == '__main__':
    main()

st.markdown("   ")
st.markdown("   ")
st.markdown("   ")
st.markdown("   ")
st.markdown("### 👨🏼‍💻  For more support contact the Engineering Team: engineer@hi-paris.fr  🚀")

