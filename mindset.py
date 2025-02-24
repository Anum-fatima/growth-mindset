import streamlit as st
import pandas as pd 
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper",layout='wide')

#custom css
st.markdown (
    """
    <style>
    .st App{
          background-color : black ;
          color : white ;
    }
    </style>
    """
    ,
    unsafe_allow_html=True
)

#title qand description 
st.title ("Datasweeper sterling integrator")
st.write ("Transform your file between CSV and excel ")

#File uploader 
uploaded_files=st.file_uploader ("upload your files (accepts CSV or Excels):" , type= [ "csv","xsls"], accept_multiple_files={True} )
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext (file.name) [-1] .lowercase
        if file_ext == ".csv":
            df=pd.read_csv(file)
        elif file_ext == "xlsx":
            df= pd.read_excel(file)
        else :
            st.error (f"unsupported file type: {file_ext}")
            continue
        #File detail
        st.write("preview the head of the Dataframe")
        st.dataframe(df.head())

        #Data cleaning option
        st.subheader ("Data Cleaning Option") 
        if st.checkbox (f"clean data for {file.name}"):
           col1  , col2 = st.columns(2)
           with col1: 
            if st.button (f"Remove duplicates from the file:{file.name}"):
              df.drop_duplicates (inplace=True)
            st.write("Duplicates Removed!")
            with col2:
                       if st.button (f"Fill missing values for {file.name}"):
                        numeric_cols =df.select_dtypes(include=['number']).columns

                        df [numeric_cols]=df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("Missing values have been filled!")

                        st.subheader("select column to keep")
                        columns = st.multiselect(f"choose column for {file.name}",df.columns,default=df.columns)

                        df.df[columns]

                        #Data visualization 
                        st.subheader("Data visualization")
                        if st.checkbox (f"show visualization for {file.name}"):
                            st.bar_chart(df.select_dtypes(include={'number'} .iloc [:,:2]))

                            #conversation option 
                            st.subheader("conversation option")
                            conversation_type = st.radio (f"convert {file.name} to:", ["cvs" ,"Excel" ] , key = file.name)

                            if st.button(f"convert {file.name}"):
                                buffer=BytesIO()
                                if conversation_type=="cvs":
                                    df.to.cvs (buffer , index = False)
                                    file_name = file.name.replace (file_ext,".cvs")
                                    mime_type = "text/csv"
        elif conversation_type == "Excel":
            df.to.to_excel (buffer,index=False)
            file_name=file.name.replace(file_ext,"xsls")
            mime_type="application/vnd.openxml formats-office documents . spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"download {file.name} as {conversation_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

            st.success("all files processed successfully")


