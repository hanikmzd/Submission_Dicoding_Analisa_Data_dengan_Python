import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the app
st.title("E-Commerce Data Visualization with Two Datasets")

# File uploaders for two CSV files
st.subheader("Upload Files")
file1 = st.file_uploader("Upload the first CSV file (Order Items)", type=["csv"])
file2 = st.file_uploader("Upload the second CSV file (Products)", type=["csv"])

if file1 and file2:
    # Load both datasets
    order_items = pd.read_csv(file1)
    products = pd.read_csv(file2)

    # Display both datasets
    st.subheader("Dataset 1: Order Items")
    st.dataframe(order_items)

    st.subheader("Dataset 2: Products")
    st.dataframe(products)

    # Merge the datasets if needed
    st.subheader("Merged Dataset")
    merged_data = pd.merge(order_items, products, on="product_id", how="inner")
    st.dataframe(merged_data)

    # Descriptive statistics for the merged dataset
    st.subheader("Descriptive Statistics for Merged Data")
    st.write(merged_data.describe())

    # Visualizations
    st.subheader("Visualizations")

    # Bar chart: Top 5 categories by total sales
    merged_data["total_sales"] = merged_data["price"] * merged_data["quantity"]
    sales_by_category = merged_data.groupby("category")["total_sales"].sum().sort_values(ascending=False)
    
    st.bar_chart(sales_by_category.head(5))

    # Histogram for product prices
    st.subheader("Price Distribution")
    fig, ax = plt.subplots()
    sns.histplot(merged_data["price"], kde=True, ax=ax)
    ax.set_title("Price Distribution")
    st.pyplot(fig)
