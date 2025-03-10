import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import plotly.express as px

# Judul aplikasi
st.title("Dashboard Analisis Bike Sharing Indonesia 🚴")

# Tentukan path file data
file_path = "dashboard/all_data.csv"

# Load dataset dengan pengecekan error
def load_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"File tidak ditemukan: {file_path}")
        return None
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
        return df
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
        return None

# Panggil fungsi load_data
all_df = load_data(file_path)

# Tampilkan dataset jika berhasil dimuat
if all_df is not None:
    st.write("📊 **Lima Data Pertama dari Dataset:**")
    st.dataframe(all_df.head())

# Sidebar untuk navigasi
def sidebar_content():
    st.sidebar.title("🚴Bike Sharing Indonesia 🚴")
    st.sidebar.image("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgCN4iLSSXFyeOfz-MllnS2rmz9KEZzJeMkeHnqdNP5pf5VLMK5m_dEhGQ3p4MxquaGLaON473NG6kYCWMu_kFf7ZVufgiNnivIkFIT7s38RAd6Mw3M0Y6VwWqA7YnFmQlxwbI5RIpiGb4f78Cpizupi2X7sSCJOcchD8G_W69KwhuU6nZtg-nJLpIWtA/s1200/sewa%20sepeda%20gbk.png", use_container_width=True)
    st.sidebar.markdown("## 📊 Informasi Peminjaman")    
    # Toggle interaktif
    show_summary = st.sidebar.checkbox("📌 Tampilkan Ringkasan Informasi", value=True)
    show_visualizations = st.sidebar.checkbox("📊 Tampilkan Visualisasi", value=True)
    return show_summary, show_visualizations

show_summary, show_visualizations = sidebar_content()

# Ringkasan informasi
if show_summary and all_df is not None:
    st.subheader("Ringkasan Informasi")
    st.write(f"Jumlah data: {all_df.shape[0]} baris dan {all_df.shape[1]} kolom")
    st.write("Statistik Deskriptif:")
    st.write(all_df.describe())

# Visualisasi data
if show_visualizations and all_df is not None:
    st.subheader("Visualisasi Data")
    
    # 1. Tren jumlah sepeda yang dipinjam dalam sehari selama satu tahun
    all_df['dteday'] = pd.to_datetime(all_df['dteday'])
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(all_df['dteday'], all_df['cnt_day'], label='Jumlah Peminjaman Sepeda', color='blue')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Sepeda yang Dipinjam')
    ax.set_title('Tren Jumlah Sepeda yang Dipinjam dalam Setahun')
    ax.legend()
    fig.autofmt_xdate()
    with st.expander("ℹ️ **Penjelasan Tren Peminjaman Sepeda**"):
        st.write("""
        - Grafik ini menunjukkan bagaimana jumlah sepeda yang dipinjam bervariasi sepanjang tahun.  
        - Kita dapat melihat adanya pola musiman, dengan periode tertentu memiliki jumlah peminjaman lebih tinggi dibandingkan periode lainnya.  
        """)
    st.pyplot(fig)
    
    # 2. Hubungan antara suhu dan peminjaman sepeda
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.regplot(x=all_df['temp_day'], y=all_df['cnt_day'], scatter_kws={'alpha': 0.6}, line_kws={'color': 'red'}, ax=ax2)
    ax2.set_xlabel('Suhu Normalisasi (temp)')
    ax2.set_ylabel('Jumlah Sepeda yang Dipinjam')
    ax2.set_title('Hubungan antara Suhu dan Peminjaman Sepeda dengan Regresi')
    with st.expander("ℹ️ **Penjelasan Hubungan Suhu & Peminjaman Sepeda**"):
        st.write("""
        - Grafik ini menunjukkan hubungan antara suhu dan jumlah sepeda yang dipinjam.  
        - Kita dapat melihat **tren positif**, di mana **semakin tinggi suhu, semakin banyak sepeda yang dipinjam**.  
        - Garis merah menunjukkan **tren regresi**, yang mengindikasikan pola umum dalam data.  
        """)
    st.pyplot(fig2)
    
    # 3. Persentase peminjaman sepeda pada hari kerja vs hari libur
    workingday_counts = all_df.groupby("workingday_day")["cnt_day"].sum()
    labels = ["Libur (0)", "Hari Kerja (1)"]
    colors = ["#ffcccb", "#a0d8ef"]
    fig3, ax3 = plt.subplots(figsize=(6, 6))
    ax3.pie(workingday_counts, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90, wedgeprops={"edgecolor": "black"})
    ax3.set_title("Persentase Peminjaman Sepeda pada Hari Kerja vs Libur")
    with st.expander("ℹ️ **Penjelasan Persentase Peminjaman Sepeda**"):
        st.write("""
        - Pie chart ini menunjukkan proporsi peminjaman sepeda pada hari kerja dibandingkan dengan hari libur.  
        - **Jika proporsi lebih besar pada hari kerja**, berarti banyak orang menggunakan sepeda untuk aktivitas sehari-hari seperti bekerja atau sekolah.  
        - **Sebaliknya, jika proporsi lebih besar pada hari libur**, ini menunjukkan bahwa sepeda lebih sering digunakan untuk rekreasi.  
        """)
    st.pyplot(fig3)
    
    # 4. Rata-rata peminjaman sepeda berdasarkan kondisi cuaca
    df_grouped = all_df.groupby("weathersit_day")["cnt_day"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = ["lightblue", "lightcoral", "lightgreen"]  # Warna lebih soft
    ax.bar(df_grouped["weathersit_day"], df_grouped["cnt_day"], color=colors)
    ax.set_title("Rata-rata Peminjaman Sepeda Berdasarkan Kondisi Cuaca", fontsize=14)
    ax.set_xlabel("Kondisi Cuaca (1=Cerah, 2=Berawan, 3=Hujan/Salju)", fontsize=12)
    ax.set_ylabel("Rata-rata Jumlah Sepeda yang Dipinjam", fontsize=12)
    with st.expander("ℹ️ **Rata-rata peminjaman berdasarkan kondisi cuaca**"):
        st.write("""
            - **Grafik ini menggambarkan hubungan antara kondisi cuaca dan jumlah peminjaman sepeda.**  
            - **Tren yang terlihat:**  
                - 🚴‍♂️ Saat **cuaca cerah**, peminjaman sepeda lebih tinggi.  
                - 🌥️ Saat **berawan**, peminjaman sedikit menurun.  
                - 🌧️ Saat **hujan atau salju**, jumlah peminjaman sepeda menurun drastis.  
            """)
    st.pyplot(fig)
    
# Copyright
st.markdown("---")
st.markdown("© 2025 Tiesya Andriani R - Proyek Analisis Data dengan Python")
