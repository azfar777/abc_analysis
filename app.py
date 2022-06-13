import streamlit as st
import numpy as np
import pandas as pd
import inventorize as ivt
import plotly.express as px
import matplotlib.pyplot as plt

st.title("Segmentation")
st.write("You can use this app to explore and perform abc analysis on your data set")

def home():
    from PIL import Image
    image = Image.open("image.jpg")
    st.image(image, caption = "Difference between A,B and C")
    
def describe():
    st.header("Data Statistics")
    st.write(df.describe())
    
def data():
    st.header("Data")
    st.write(df)
    
def abc():
    st.write("Please select the parameter you want to group by your data")
    col1, col2, col3 = st.columns(2)
    
    value_1 = col1.selectbox('Select the first parameter', options=df.columns)
    value_2 = col2.selectbox('Select the second parameter', options=df.columns)
    st.write("To filter your search, click anywhere on the table and press CTRL + F")
    st.write("Scroll down to see the plots")
    grouped = df.groupby(value_1).agg(total_sales = (value_2, np.sum)).reset_index()
    abc = ivt.ABC(grouped[[value_1,"total_sales"]])
    abc = abc.reset_index()
    abc.drop("index",axis = 1, inplace = True)
    st.write(abc)
    csv = abc.to_csv().encode('utf-8')
    st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)
    fig1 = px.histogram(abc, x = "Category", barmode="group")
    st.plotly_chart(fig1)
    
    fig2 = px.bar(abc, x = "Category", y = "total_sales")
    st.plotly_chart(fig2)    
        
    
    
st.sidebar.title("Navigation")
file = st.sidebar.file_uploader("Please upload your file here")
options = st.sidebar.radio("Select item which you want to dsiplay", options = ["Home","Data","Data Summary",
                                                                               "abc analysis"
                                                                               ])
if file is not None:
    df = pd.read_csv(file)
    if "Unnamed: 0" in df.columns:
        df.drop("Unnamed: 0",axis = 1)
    

if options == "Home":
    home()
    
elif options == "Data Summary":
    describe()
    
elif options == "Data":
    data()

elif options == "abc analysis":
    abc()
