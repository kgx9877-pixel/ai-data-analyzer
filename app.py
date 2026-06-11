import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# PAGE CONFIG
st.set_page_config(page_title="AI Data Analyst Dashboard", layout="wide")

# TITLE
st.title("📊 AI Data Analyst Dashboard")
st.subheader("Upload CSV → Get Instant Insights, Statistics & Charts")

# FILE UPLOAD
uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded_file is not None:

    # READ CSV
    df = pd.read_csv(uploaded_file)

    # DATA PREVIEW
    st.markdown("---")
    st.header("📂 Data Preview")
    st.dataframe(df)

    # DATASET INFO
    st.markdown("---")
    st.header("📊 Dataset Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    # SEARCH DATA
    st.markdown("---")
    st.header("🔍 Search Data")

    search = st.text_input("Enter keyword")

    if search:
        filtered_df = df[
            df.astype(str)
            .apply(lambda x: x.str.contains(search, case=False, na=False))
            .any(axis=1)
        ]

        st.write("### Search Results")
        st.dataframe(filtered_df)

    # COLUMN SELECT
    st.markdown("---")
    st.header("📌 Column Analysis")

    column = st.selectbox("Choose a Column", df.columns)

    st.write("### Selected Column:", column)

    # STATISTICS
    st.markdown("---")
    st.header("📊 Statistics")

    if pd.api.types.is_numeric_dtype(df[column]):
        st.write(df[column].describe())
    else:
        st.warning("⚠️ Statistics available only for numeric columns")

    # MISSING VALUES
    st.markdown("---")
    st.header("❗ Missing Values")

    st.dataframe(df.isnull().sum().reset_index().rename(
        columns={"index": "Column", 0: "Missing Values"}
    ))

    # DATA TYPES
    st.markdown("---")
    st.header("🧾 Data Types")

    st.dataframe(df.dtypes.astype(str).reset_index().rename(
        columns={"index": "Column", 0: "Data Type"}
    ))

    # FULL SUMMARY
    st.markdown("---")
    st.header("📈 Full Dataset Summary")

    try:
        st.dataframe(df.describe(include='all'))
    except:
        st.write("Summary not available")

    # CHARTS
    st.markdown("---")
    st.header("📊 Visualizations")

    if pd.api.types.is_numeric_dtype(df[column]):

        st.subheader("Bar Chart")
        st.bar_chart(df[column])

        st.subheader("Line Chart")
        st.line_chart(df[column])

        st.subheader("Histogram")

        fig, ax = plt.subplots()
        ax.hist(df[column].dropna(), bins=20)
        ax.set_title(f"Histogram of {column}")
        st.pyplot(fig)

        st.subheader("Box Plot")

        fig2, ax2 = plt.subplots()
        ax2.boxplot(df[column].dropna())
        ax2.set_title(f"Box Plot of {column}")
        st.pyplot(fig2)

    else:

        st.subheader("Category Count")

        st.bar_chart(df[column].value_counts())

        st.subheader("Pie Chart")

        fig3, ax3 = plt.subplots(figsize=(6, 6))
        df[column].value_counts().plot(
            kind="pie",
            autopct="%1.1f%%",
            ax=ax3
        )
        ax3.set_ylabel("")
        st.pyplot(fig3)

    # CORRELATION HEATMAP
    st.markdown("---")
    st.header("🔥 Correlation Heatmap")

    numeric_df = df.select_dtypes(include=["number"])

    if len(numeric_df.columns) > 1:

        fig4, ax4 = plt.subplots(figsize=(10, 6))

        sns.heatmap(
            numeric_df.corr(),
            annot=True,
            cmap="coolwarm",
            ax=ax4
        )

        st.pyplot(fig4)

    else:
        st.info("Need at least 2 numeric columns for heatmap")

    # TOP AND BOTTOM VALUES
    st.markdown("---")

    if pd.api.types.is_numeric_dtype(df[column]):

        st.header("🏆 Top & Bottom Values")

        col1, col2 = st.columns(2)

        with col1:
            st.write("### Top 5 Values")
            st.write(df[column].nlargest(5))

        with col2:
            st.write("### Bottom 5 Values")
            st.write(df[column].nsmallest(5))

    # AI INSIGHT
    st.markdown("---")
    st.header("🤖 AI Insight")

    if pd.api.types.is_numeric_dtype(df[column]):

        avg = df[column].mean()
        median = df[column].median()

        st.write("Average:", round(avg, 2))
        st.write("Median:", round(median, 2))
        st.write("Maximum:", df[column].max())
        st.write("Minimum:", df[column].min())

        if avg > median:
            st.success(
                "📈 Positive trend detected. Average is higher than median."
            )
        elif avg < median:
            st.warning(
                "📉 Data may contain lower values affecting average."
            )
        else:
            st.info(
                "📊 Average and median are equal."
            )

    else:
        st.info("AI insight available only for numeric columns")

    # AI SUMMARY
    st.markdown("---")
    st.header("📝 AI Summary")

    st.write(
        f"""
        This dataset contains **{df.shape[0]} rows**
        and **{df.shape[1]} columns**.

        Selected column: **{column}**
        """
    )

    # DOWNLOAD DATA
    st.markdown("---")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Dataset",
        data=csv,
        file_name="processed_data.csv",
        mime="text/csv"
    )

else:
    st.info("⬆ Please upload a CSV file to begin analysis.")