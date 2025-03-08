import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")

# Apply custom CSS
st.markdown(
    """
    <style>
        body {
            background-color: #1E1E1E;
            color: #FFFFFF;
            font-family: Arial, sans-serif;
        }
        .css-1aumxhk, .stButton > button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px;
        }
        .stTextInput, .stFileUploader, .stRadio, .stMultiSelect, .stDataFrame {
            border: 1px solid #4CAF50;
            border-radius: 5px;
            padding: 5px;
        }
        .stMarkdown h1 {
            color: #4CAF50;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("📂 File Converter & Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats effortlessly.")

files = st.file_uploader("📤 Upload CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"🧹 Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates Removed")
            st.dataframe(df.head())

        if st.checkbox(f"🛠 Handle Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
            st.success("Missing Values Filled with Mean")
            st.dataframe(df.head())

        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"⬇️ Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime_type = "text/csv"
                new_name = file.name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")

            output.seek(0)
            st.download_button("📥 Download File", file_name=new_name, data=output, mime=mime_type)

        st.success("Processing Complete!")
