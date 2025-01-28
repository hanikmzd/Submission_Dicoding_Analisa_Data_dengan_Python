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
    # Memastikan file dapat dibaca dan tidak kosong
    order_items_data = pd.read_csv(order_items_path)
    products_data = pd.read_csv(products_path)

    if order_items_data.empty or products_data.empty:
        raise ValueError("Salah satu file atau keduanya kosong.")

    # Drop missing value pada kolom product_category_name
    products_data.drop(products_data[products_data.product_category_name.isna()].index, inplace=True)

    # Memastikan kolom yang diperlukan tersedia
    if 'product_category_name' in products_data.columns and 'product_id' in order_items_data.columns:
        # Menggabungkan dataset untuk mendapatkan kategori produk terlaris
        merged_data = pd.merge(order_items_data, products_data, on='product_id', how='inner')

        if merged_data.empty:
            raise ValueError("Data hasil penggabungan kosong. Pastikan data memiliki kecocokan kolom 'product_id'.")

        # 10 Kategori Produk Terlaris
        st.subheader("10 Kategori Produk Terlaris")
        top_10_products = merged_data.groupby('product_category_name')['order_item_id'].count().nlargest(10).reset_index()

        fig1, ax1 = plt.subplots(figsize=(12, 6))
        bars = ax1.barh(top_10_products['product_category_name'], top_10_products['order_item_id'], color='skyblue')
        ax1.set_xlabel('Jumlah Produk Terjual')
        ax1.set_ylabel('Kategori Produk')
        ax1.set_title('10 Kategori Produk Terlaris')

        # Menambahkan angka pada ujung bar
        for bar, value in zip(bars, top_10_products['order_item_id']):
            ax1.text(value, bar.get_y() + bar.get_height()/2, f'{value:,}', va='center', ha='left')

        ax1.invert_yaxis()
        st.pyplot(fig1)

        # Pilihan visualisasi tren
        st.subheader("Pilih Visualisasi Tren")
        option = st.selectbox(
            "Pilih jenis tren yang ingin divisualisasikan:",
            ("Tren Jumlah Order Item per Bulan", "Tren Penjualan per Bulan")
        )

        merged_data['shipping_limit_date'] = pd.to_datetime(merged_data['shipping_limit_date'])
        merged_data['year_month'] = merged_data['shipping_limit_date'].dt.to_period('M')

        if option == "Tren Jumlah Order Item per Bulan":
            # Tren Jumlah Order Item per Bulan
            order_trend = merged_data.groupby('year_month')['order_item_id'].count().reset_index()
            order_trend.columns = ['year_month', 'order_count']
            order_trend = order_trend.sort_values(by='year_month')

            st.subheader("Tren Jumlah Order Item per Bulan")
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            ax2.plot(order_trend['year_month'].astype(str), order_trend['order_count'], marker='o')
            for i in range(len(order_trend)):
                ax2.text(x=order_trend['year_month'].astype(str).iloc[i], y=order_trend['order_count'].iloc[i], 
                        s=str(order_trend['order_count'].iloc[i]), ha='center', va='bottom', fontsize=9, color='blue')
            ax2.set_xlabel('Bulan dan Tahun')
            ax2.set_ylabel('Jumlah Order Item')
            ax2.set_title('Tren Jumlah Order Item per Bulan')
            ax2.tick_params(axis='x', rotation=45)
            st.pyplot(fig2)

        elif option == "Tren Penjualan per Bulan":
            # Tren Penjualan per Bulan
            sales_trend = merged_data.groupby('year_month')['price'].sum().reset_index()
            sales_trend.columns = ['year_month', 'order_sum']
            sales_trend = sales_trend.sort_values(by='year_month')

            st.subheader("Tren Penjualan per Bulan")
            fig3, ax3 = plt.subplots(figsize=(10, 6))
            ax3.plot(sales_trend['year_month'].astype(str), sales_trend['order_sum'], marker='o')
            for i in range(len(sales_trend)):
                ax3.text(x=sales_trend['year_month'].astype(str).iloc[i], y=sales_trend['order_sum'].iloc[i], 
                        s=f"{sales_trend['order_sum'].iloc[i]:,.2f}", ha='center', va='bottom', fontsize=9, color='blue')
            ax3.set_xlabel('Bulan dan Tahun')
            ax3.set_ylabel('Total Penjualan')
            ax3.set_title('Tren Penjualan per Bulan')
            ax3.tick_params(axis='x', rotation=45)
            st.pyplot(fig3)

    else:
        st.warning("Kolom yang diperlukan untuk visualisasi tidak ditemukan dalam dataset.")

except FileNotFoundError as e:
    st.error(f"File tidak ditemukan: {e}")
except pd.errors.EmptyDataError:
    st.error("File kosong atau tidak memiliki data untuk diproses.")
except ValueError as e:
    st.error(f"Terjadi kesalahan pada data: {e}")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
