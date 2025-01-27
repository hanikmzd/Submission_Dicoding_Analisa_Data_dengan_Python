import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the app
st.title("E-Commerce Sales Data Visualization")

# File uploaders for two CSV files
file1 = st.file_uploader("Dashboard/order_items_dataset.csv", type=["csv"])
file2 = st.file_uploader("Dashboard/products_dataset.csv", type=["csv"])

# Process only if both files are uploaded
if file1 is not None and file2 is not None:
    # Load both datasets
    try:
        order_items = pd.read_csv(file1)
        products = pd.read_csv(file2)

        # Merge the datasets
        st.subheader("Merged Dataset")
        merged_data = pd.merge(order_items, products, on="product_id", how="inner")
        st.dataframe(merged_data)

        # Descriptive statistics for the merged dataset
        st.subheader("Descriptive Statistics for Merged Data")
        st.write(merged_data.describe())

        # Add a calculated column for total sales
        merged_data["total_sales"] = merged_data["price"] * merged_data["quantity"]

        # Bar chart: Top 5 categories by total sales
        st.subheader("Top 5 Categories by Total Sales")
        sales_by_category = merged_data.groupby("category")["total_sales"].sum().sort_values(ascending=False)
        st.bar_chart(sales_by_category.head(5))

        # Histogram for product prices
        st.subheader("Price Distribution")
        fig, ax = plt.subplots()
        sns.histplot(merged_data["price"], kde=True, ax=ax)
        ax.set_title("Price Distribution")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error processing the files: {e}")
else:
    st.warning("Please upload both datasets to proceed.")
