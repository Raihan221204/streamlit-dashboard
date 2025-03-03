import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi dasar
st.set_page_config(page_title="Dashboard Analisis Pengiriman", layout="wide")

# Identitas pembuat
st.sidebar.markdown("## Dashboard oleh Muhammad Raihan MC-20")

# Membaca data CSV
file_path = r'C:\Users\MUHAMMAD RAIHAN\Downloads\dataset dicoding\final_df.csv'
final_df = pd.read_csv(file_path)

# Pastikan kolom tanggal dalam format datetime
final_df['order_estimated_delivery_date_item'] = pd.to_datetime(final_df['order_estimated_delivery_date_item'], errors='coerce')
final_df['order_delivered_customer_date_item'] = pd.to_datetime(final_df['order_delivered_customer_date_item'], errors='coerce')

# Menghitung keterlambatan pengiriman (dalam hari)
final_df['delivery_delay_days'] = (final_df['order_delivered_customer_date_item'] - final_df['order_estimated_delivery_date_item']).dt.days

# Menambahkan kolom 'on_time' untuk menandakan pengiriman tepat waktu (1) atau terlambat (0)
final_df['on_time'] = (final_df['delivery_delay_days'] <= 0).astype(int)

# Menambahkan kolom hari dalam minggu dan bulan
final_df['delivery_day_of_week'] = final_df['order_delivered_customer_date_item'].dt.dayofweek
final_df['delivery_month'] = final_df['order_delivered_customer_date_item'].dt.month

# Header
st.title("📦 Dashboard Analisis Pengiriman")
st.markdown("### Analisis Ketepatan Waktu dan Pola Pengiriman")

# Distribusi Keterlambatan Pengiriman
st.subheader("📊 Distribusi Keterlambatan Pengiriman")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(final_df['delivery_delay_days'], kde=True, bins=30, color='lightgreen', ax=ax)
ax.set_title('Distribusi Keterlambatan Pengiriman')
ax.set_xlabel('Keterlambatan Pengiriman (hari)')
ax.set_ylabel('Frekuensi')
st.pyplot(fig)

# Keterlambatan Berdasarkan Hari dalam Minggu
st.subheader("📅 Keterlambatan Berdasarkan Hari dalam Minggu")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x='delivery_day_of_week', y='delivery_delay_days', data=final_df, palette='Set2', ax=ax)
ax.set_title('Keterlambatan Pengiriman Berdasarkan Hari dalam Minggu')
ax.set_xlabel('Hari dalam Minggu')
ax.set_ylabel('Keterlambatan Pengiriman (hari)')
ax.set_xticklabels(['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'])
st.pyplot(fig)

# Pengaruh Status Pengiriman terhadap Ketepatan Waktu
if 'order_status_item' in final_df.columns:
    on_time_status = final_df.groupby('order_status_item')['on_time'].mean().reset_index()
    
    st.subheader("📌 Pengaruh Status Pengiriman terhadap Ketepatan Waktu")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='order_status_item', y='on_time', data=on_time_status, palette='viridis', ax=ax)
    ax.set_title('Persentase Pengiriman Tepat Waktu per Status Pengiriman')
    ax.set_xlabel('Status Pengiriman')
    ax.set_ylabel('Persentase Tepat Waktu')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)
else:
    st.markdown("⚠️ **Kolom 'order_status_item' tidak tersedia dalam dataset.**")

# Kesimpulan
st.subheader("📌 Kesimpulan")
st.markdown("""
1. **Keterlambatan Pengiriman**: Rata-rata keterlambatan sekitar -11.88 hari. Keterlambatan lebih sering terjadi pada akhir pekan dan bulan tertentu seperti Juli dan Desember.
2. **Pola Musiman**: Pengiriman lebih tepat waktu pada bulan tertentu, dan status pengiriman "delivered" memiliki tingkat ketepatan waktu yang lebih tinggi.
3. **Hari Pengiriman**: Keterlambatan lebih sering terjadi pada hari Sabtu dan Minggu.
4. **Status Pengiriman**: Status 'delivered' memiliki tingkat ketepatan waktu tertinggi dibandingkan status lainnya.
""")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("📌 **Dibuat oleh Muhammad Raihan MC-20**")
