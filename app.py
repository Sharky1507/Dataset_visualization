import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Data Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

# Sidebar - File upload
st.sidebar.header("Upload your dataset")
uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV, XLS, or XLSX file",
    type=["csv", "xls", "xlsx"]
)

# Load data
@st.cache_data
def load_data(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

if uploaded_file is not None:
    df = load_data(uploaded_file)
    
    if df is not None:
        st.title("Dataset Analysis Dashboard")
        st.markdown("---")
        
        st.subheader("Dataset Preview")
        st.dataframe(df.head(), use_container_width=True)
        
        with st.expander("Dataset Overview", expanded=False):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write("**Shape**")
                st.info(f"{df.shape[0]} rows, {df.shape[1]} columns")
            with c2:
                st.write("**Columns Types**")
                dtypes = df.dtypes.value_counts()
                st.write(dtypes)
            with c3:
                st.write("**Missing Values**")
                st.write(df.isnull().sum())
        
        with st.expander("Summary Statistics", expanded=False):
            show_all = st.checkbox("Show all columns", value=False)
            if show_all:
                st.write(df.describe(include='all'))
            else:
                st.write(df.describe())
        
        st.markdown("---")
        st.subheader("Data Visualization")
        
        # Visualization controls in sidebar
        st.sidebar.header("Chart Configuration")
        chart_type = st.sidebar.selectbox(
            "Select Chart Type",
            ["Histogram", "Bar Chart", "Line Chart", "Scatter Plot", "Box Plot"]
        )
        
        if chart_type == "Histogram":
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            selected_col = st.sidebar.selectbox("Select Column", numeric_cols)
            fig = px.histogram(df, x=selected_col, title=f"Histogram of {selected_col}")
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Bar Chart":
            all_cols = df.columns.tolist()
            selected_col = st.sidebar.selectbox("Select Column", all_cols)
            fig = px.bar(df, x=selected_col, title=f"Bar Chart of {selected_col}")
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Scatter Plot":
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            x_col = st.sidebar.selectbox("Select X Column", numeric_cols)
            y_col = st.sidebar.selectbox("Select Y Column", numeric_cols)
            fig = px.scatter(df, x=x_col, y=y_col, 
                            title=f"Scatter Plot: {x_col} vs {y_col}")
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Line Chart":
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            x_col = st.sidebar.selectbox("Select X Column", df.columns)
            y_col = st.sidebar.selectbox("Select Y Column", numeric_cols)
            fig = px.line(df, x=x_col, y=y_col, 
                         title=f"Line Chart: {y_col} over {x_col}")
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Box Plot":
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            selected_col = st.sidebar.selectbox("Select Column", numeric_cols)
            fig = px.box(df, y=selected_col, title=f"Box Plot of {selected_col}")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Correlation Matrix")
        numeric_df = df.select_dtypes(include=np.number)
        if not numeric_df.empty:
            corr = numeric_df.corr()
            fig = px.imshow(corr,
                            text_auto=True,
                            aspect="auto",
                            title="Correlation Heatmap")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No numeric columns to compute correlations.")
        
        if st.checkbox("Show Full Dataset"):
            st.subheader("Raw Data")
            st.dataframe(df, use_container_width=True)
else:
    st.info("Please upload a dataset through the left sidebar to begin analysis.")

