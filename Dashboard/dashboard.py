import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Dashboard
st.title("Dashboard Visualisasi Data")

# Memuat File Data
order_items_path = "Dashboard/order_items_dataset.csv"
products_path = "Dashboard/products_dataset.csv"

try:
    # Membaca dataset
    order_items_data = pd.read_csv(order_items_path)
    products_data = pd.read_csv(products_path)
    st.success("Dataset berhasil dimuat!")

    # Menampilkan preview data
    st.subheader("Preview Data Order Items")
    st.dataframe(order_items_data.head())

    st.subheader("Preview Data Products")
    st.dataframe(products_data.head())

    # Menampilkan informasi dataset
    st.subheader("Informasi Dataset")
    st.write("Order Items - Jumlah Baris dan Kolom:", order_items_data.shape)
    st.write("Products - Jumlah Baris dan Kolom:", products_data.shape)

    # Statistik deskriptif
    st.write("Statistik Deskriptif Order Items:")
    st.write(order_items_data.describe())

    st.write("Statistik Deskriptif Products:")
    st.write(products_data.describe())

    # Pilihan kolom untuk visualisasi
    st.subheader("Visualisasi Data")
    numeric_columns_order = order_items_data.select_dtypes(include=['float64', 'int64']).columns
    numeric_columns_products = products_data.select_dtypes(include=['float64', 'int64']).columns

    if len(numeric_columns_order) > 0 or len(numeric_columns_products) > 0:
        col1, col2 = st.columns(2)

        # Histogram
        with col1:
            st.write("Histogram")
            selected_column_order = st.selectbox("Pilih Kolom untuk Histogram (Order Items)", numeric_columns_order, key="hist_order")
            selected_column_products = st.selectbox("Pilih Kolom untuk Histogram (Products)", numeric_columns_products, key="hist_products")

            # Order Items Histogram
            fig1, ax1 = plt.subplots()
            sns.histplot(order_items_data[selected_column_order], kde=True, ax=ax1)
            ax1.set_title(f"Histogram of {selected_column_order} (Order Items)")
            st.pyplot(fig1)

            # Products Histogram
            fig2, ax2 = plt.subplots()
            sns.histplot(products_data[selected_column_products], kde=True, ax=ax2)
            ax2.set_title(f"Histogram of {selected_column_products} (Products)")
            st.pyplot(fig2)

        # Scatter Plot
        with col2:
            st.write("Scatter Plot (Order Items)")
            x_column_order = st.selectbox("Pilih Kolom X (Order Items)", numeric_columns_order, key="scatter_x_order")
            y_column_order = st.selectbox("Pilih Kolom Y (Order Items)", numeric_columns_order, key="scatter_y_order")
            fig3, ax3 = plt.subplots()
            sns.scatterplot(x=order_items_data[x_column_order], y=order_items_data[y_column_order], ax=ax3)
            ax3.set_title(f"Scatter Plot of {x_column_order} vs {y_column_order} (Order Items)")
            st.pyplot(fig3)

        # Heatmap
        st.subheader("Heatmap Korelasi")
        if len(numeric_columns_order) > 1:
            fig4, ax4 = plt.subplots()
            sns.heatmap(order_items_data[numeric_columns_order].corr(), annot=True, cmap="coolwarm", ax=ax4)
            ax4.set_title("Correlation Heatmap (Order Items)")
            st.pyplot(fig4)

        if len(numeric_columns_products) > 1:
            fig5, ax5 = plt.subplots()
            sns.heatmap(products_data[numeric_columns_products].corr(), annot=True, cmap="coolwarm", ax=ax5)
            ax5.set_title("Correlation Heatmap (Products)")
            st.pyplot(fig5)

    else:
        st.warning("Dataset Anda tidak memiliki kolom numerik untuk divisualisasikan.")

except FileNotFoundError as e:
    st.error(f"File tidak ditemukan: {e}")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
