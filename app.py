import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Data Analyzer", layout="wide")

st.title("📊 AI Data Analyzer (Free Version)")
st.write("Upload CSV → Analyze → Ask Smart Questions")

# 📂 Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 📂 Preview
    st.subheader("📂 Data Preview")
    st.dataframe(df)

    # 📊 Info
    st.subheader("📊 Dataset Info")
    col1, col2 = st.columns(2)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

    # 📌 Column Analysis
    st.subheader("📌 Column Analysis")
    column = st.selectbox("Select column", df.columns)

    if pd.api.types.is_numeric_dtype(df[column]):
        st.subheader("📊 Statistics")
        st.write("Mean:", df[column].mean())
        st.write("Median:", df[column].median())
        st.write("Max:", df[column].max())
        st.write("Min:", df[column].min())

        st.subheader("📈 Charts")
        st.bar_chart(df[column])
        st.line_chart(df[column])

    # ❗ Missing values
    st.subheader("❗ Missing Values")
    st.write(df.isnull().sum())

    # 🧾 Data types
    st.subheader("🧾 Data Types")
    st.write(df.dtypes)

    # 🤖 Smart AI (NO API)
    st.subheader("🤖 Ask Questions About Your Data")

    question = st.text_input("Ask your question (e.g., average, max, min, sum)")

    if question:
        q = question.lower()
        numeric_df = df.select_dtypes(include='number')

        if numeric_df.empty:
            st.warning("No numeric data available")
        else:
            if "average" in q or "mean" in q:
                result = numeric_df.mean().mean()
                st.success(f"The average value across numeric columns is {result:.2f}")

            elif "max" in q:
                result = numeric_df.max().max()
                st.success(f"The maximum value in dataset is {result}")

            elif "min" in q:
                result = numeric_df.min().min()
                st.success(f"The minimum value in dataset is {result}")

            elif "sum" in q:
                result = numeric_df.sum().sum()
                st.success(f"The total sum of numeric data is {result}")

            elif "rows" in q:
                st.success(f"The dataset has {df.shape[0]} rows")

            elif "columns" in q:
                st.success(f"Columns are: {list(df.columns)}")

            else:
                st.info("Try asking: average, max, min, sum, rows, columns")