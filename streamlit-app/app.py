import streamlit as st
from menu_home import display_home
from menu_data_collection import display_data_collection
from menu_data_annotation import display_data_annotation
from menu_eda import display_eda
from menu_data_preprocessing import display_data_preprocessing


st.set_page_config(layout="wide")

# menu sidebar
list_menu = ['Home', 'Data Collection', 'Data Annotation', 'Exploratory Data Analysis', 'Data Preprocessing', 'Modeling', 'Evaluation', 'Deployment']
menu_choice = st.sidebar.selectbox("Select a menu", list_menu)

### MENU: HOME ###
if menu_choice == 'Home':
    display_home()
    
### MENU: DATA COLLECTION ###
if menu_choice == 'Data Collection':
    display_data_collection()

### MENU: DATA ANNOTATION ###
if menu_choice == 'Data Annotation':
    display_data_annotation()

### MENU: EXPLORATORY DATA ANALYSIS ###
if menu_choice == 'Exploratory Data Analysis':
    display_eda()

### MENU: DATA PREPROCESSING ###
if menu_choice == 'Data Preprocessing':
    display_data_preprocessing()