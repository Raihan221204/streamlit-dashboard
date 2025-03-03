import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import gdown 

# Konfigurasi dasar Streamlit
st.set_page_config(page_title="Dashboard Analisis Pengiriman", layout="wide")

# Identitas pembuat
st.sidebar.markdown("## Dashboard oleh Muhammad Raihan MC-20")

# URL Google Drive untuk mengunduh dataset
file_id = "1E2OVeWBPrbZ6gXnXa9VByhLpMQ6wAEyP"
gdrive_url = f"https://drive.google.com/uc?id={file_id}"

# Fungsi untuk mengunduh dan memuat data
@st.cache_data
def load_data():
    try:
        file_path = "final_df.csv"
        gdown.download(gdrive_url, file_path, quiet=False)
        df = pd.read_csv(file_path)

        # Pastikan kolom tanggal dalam format datetime
        date_cols = ['order_estimated_delivery_date_item', 'order_delivered_customer_date_item', 'order_purchase_timestamp_item']
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')

        # Menghitung keterlambatan pengiriman (dalam hari)
        df['delivery_delay_days'] = (df['order_delivered_customer_date_item'] - df['order_estimated_delivery_date_item']).dt.days
        df['on_time'] = (df['delivery_delay_days'] <= 0).astype(int)
        
        # Menambahkan kolom hari dalam minggu dan bulan
        df['delivery_day_of_week'] = df['order_delivered_customer_date_item'].dt.dayofweek
        df['delivery_month'] = df['order_delivered_customer_date_item'].dt.month

        return df
    except Exception as e:
        st.error(f"❌ Gagal memuat data: {e}")
        return None

# Load data
final_df = load_data()

if final_df is not None:
    # 🔥 **Fitur Interaktif - Filter Tanggal**
    st.sidebar.subheader("📅 Filter Data Berdasarkan Rentang Tanggal")

    min_date = final_df['order_purchase_timestamp_item'].min()
    max_date = final_df['order_purchase_timestamp_item'].max()

    start_date = st.sidebar.date_input("Mulai Tanggal", min_date)
    end_date = st.sidebar.date_input("Akhir Tanggal", max_date)

    start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)

    # Filter data
    filtered_df = final_df[(final_df['order_purchase_timestamp_item'] >= start_date) & (final_df['order_purchase_timestamp_item'] <= end_date)]
    st.sidebar.write(f"📊 Data yang ditampilkan: {len(filtered_df)} transaksi")

    # Header
    st.title("📦 Dashboard Analisis Pengiriman")
    st.markdown("### Analisis Ketepatan Waktu dan Pola Pengiriman")

    if not filtered_df.empty:
        # 🔥 Distribusi Keterlambatan Pengiriman
        st.subheader("📊 Distribusi Keterlambatan Pengiriman")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(filtered_df['delivery_delay_days'], kde=True, bins=30, color='lightgreen', ax=ax)
        ax.set_title('Distribusi Keterlambatan Pengiriman')
        ax.set_xlabel('Keterlambatan Pengiriman (hari)')
        ax.set_ylabel('Frekuensi')
        st.pyplot(fig)

        # 🔥 Keterlambatan Berdasarkan Hari dalam Minggu
        st.subheader("📅 Keterlambatan Berdasarkan Hari dalam Minggu")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.boxplot(x='delivery_day_of_week', y='delivery_delay_days', data=filtered_df, palette='Set2', ax=ax)
        ax.set_title('Keterlambatan Pengiriman Berdasarkan Hari dalam Minggu')
        ax.set_xlabel('Hari dalam Minggu')
        ax.set_ylabel('Keterlambatan Pengiriman (hari)')
        ax.set_xticklabels(['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'])
        st.pyplot(fig)

        # 🔥 Pengaruh Status Pengiriman terhadap Ketepatan Waktu
        if 'order_status_item' in filtered_df.columns:
            on_time_status = filtered_df.groupby('order_status_item')['on_time'].mean().reset_index()
            st.subheader("📌 Pengaruh Status Pengiriman terhadap Ketepatan Waktu")
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(x='order_status_item', y='on_time', data=on_time_status, palette='viridis', ax=ax)
            ax.set_title('Persentase Pengiriman Tepat Waktu per Status Pengiriman')
            ax.set_xlabel('Status Pengiriman')
            ax.set_ylabel('Persentase Tepat Waktu')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            st.pyplot(fig)
        
        # 🔥 Kesimpulan Otomatis
        avg_delay = filtered_df['delivery_delay_days'].mean()
        if not filtered_df['delivery_day_of_week'].isna().all():
            most_delayed_day = filtered_df.groupby('delivery_day_of_week')['delivery_delay_days'].mean().idxmax()
            most_delayed_day_name = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"][int(most_delayed_day)]
        else:
            most_delayed_day_name = "Tidak diketahui"

        on_time_percentage = filtered_df['on_time'].mean() * 100
        worst_status = filtered_df.groupby('order_status_item')['delivery_delay_days'].mean().idxmax() if 'order_status_item' in filtered_df.columns else "Tidak diketahui"

        st.subheader("📌 Kesimpulan Otomatis Berdasarkan Data yang Difilter")
        st.markdown(f"""
        1. **Rata-rata Keterlambatan**: Dalam rentang **{start_date.date()} hingga {end_date.date()}**, keterlambatan pengiriman rata-rata adalah **{avg_delay:.2f} hari**.
        2. **Hari Keterlambatan Tertinggi**: Hari dengan rata-rata keterlambatan tertinggi adalah **{most_delayed_day_name}**.
        3. **Persentase Pengiriman Tepat Waktu**: Sebanyak **{on_time_percentage:.2f}%** pengiriman tiba tepat waktu.
        4. **Status Pengiriman dengan Keterlambatan Tertinggi**: Status dengan keterlambatan pengiriman paling tinggi adalah **{worst_status}**.
        """)
    else:
        st.warning("⚠️ Tidak ada data yang tersedia setelah filter diterapkan.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("📌 **Dibuat oleh Muhammad Raihan MC-20**")
