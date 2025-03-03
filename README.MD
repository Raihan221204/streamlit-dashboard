# 📦 Dashboard Analisis Pengiriman

Dashboard ini dibuat menggunakan **Streamlit** untuk menganalisis keterlambatan pengiriman berdasarkan dataset tertentu.

---

## 🚀 Cara Menjalankan Dashboard

### 1. **Persyaratan**
Pastikan Anda sudah menginstal **Python 3.7+** dan memiliki paket yang dibutuhkan:

```sh
pip install streamlit pandas seaborn matplotlib gdown
```

### 2. **Menjalankan Dashboard Secara Lokal**
1. Clone repositori ini atau unduh file sumbernya:
   ```sh
   git clone https://github.com/username/repository-name.git
   cd repository-name
   ```
2. Jalankan Streamlit:
   ```sh
   streamlit run dashboard.py
   ```
3. Buka browser dan akses **`http://localhost:8501`**.

---

## 📂 Menggunakan Dataset dari Google Drive
Dashboard ini membaca dataset dari Google Drive menggunakan **gdown**. Untuk memastikan dataset bisa diakses:

1. **Dapatkan Link Google Drive**
   - Pastikan file CSV Anda di Google Drive memiliki akses **"Anyone with the link"**.
   - Salin ID file dari URL Google Drive, misalnya:
     ```
     https://drive.google.com/file/d/1E2OVeWBPrbZ6gXnXa9VByhLpMQ6wAEyP/view?usp=sharing
     ```
     **ID File:** `1E2OVeWBPrbZ6gXnXa9VByhLpMQ6wAEyP`

2. **Tambahkan ke Kode Python**
   ```python
   import gdown
   url = 'https://drive.google.com/uc?id=1E2OVeWBPrbZ6gXnXa9VByhLpMQ6wAEyP'
   output = 'dataset.csv'
   gdown.download(url, output, quiet=False)
   ```

3. **Pastikan File Terunduh Sebelum Diproses**
   ```python
   import pandas as pd
   final_df = pd.read_csv('dataset.csv')
   ```

---

## 🌍 Menjalankan di Streamlit Cloud
Jika ingin **deploy ke Streamlit Cloud**, ikuti langkah ini:

1. **Tambahkan file `requirements.txt`** di GitHub:
   ```
   streamlit
   pandas
   seaborn
   matplotlib
   gdown
   ```

2. **Push ke GitHub**, lalu deploy di [Streamlit Cloud](https://share.streamlit.io/).

3. Jika ada perubahan di GitHub, **restart aplikasi** di dashboard Streamlit Cloud.

---

## 👤 Pembuat
**Muhammad Raihan MC-20**

