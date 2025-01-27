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
    # Membaca dataset dengan menangani potensi masalah parsing
    order_items_data = pd.read_csv(order_items_path, on_bad_lines='skip')
    products_data = pd.read_csv(products_path, on_bad_lines='skip')
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

    # Visualisasi: 10 Kategori Produk Terlaris
    st.subheader("Visualisasi: 10 Kategori Produk Terlaris")
    if 'product_category_name' in order_items_data.columns and 'order_item_id' in order_items_data.columns:
        top_10_products = order_items_data.groupby('product_category_name')['order_item_id'].count().nlargest(10).reset_index()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.barh(top_10_products['product_category_name'], top_10_products['order_item_id'], color='skyblue')
        ax.set_xlabel('Jumlah Produk Terjual')
        ax.set_ylabel('Kategori Produk')
        ax.set_title('10 Kategori Produk Terlaris')

        # Menambahkan angka pada ujung bar
        for bar, value in zip(bars, top_10_products['order_item_id']):
            ax.text(value, bar.get_y() + bar.get_height()/2, f'{value:,}', va='center', ha='left')

        ax.invert_yaxis()
        st.pyplot(fig)
    else:
        st.warning("Kolom 'product_category_name' atau 'order_item_id' tidak ditemukan dalam dataset.")

except FileNotFoundError as e:
    st.error(f"File tidak ditemukan: {e}")
except pd.errors.EmptyDataError:
    st.error("File kosong atau tidak memiliki data untuk diproses.")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
