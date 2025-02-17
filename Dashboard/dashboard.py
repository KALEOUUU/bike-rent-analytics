import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Dashboard
st.title('Bike Rent Analytic')

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv('dataset_all.csv')
    # Konversi kolom dteday ke datetime
    df['dteday'] = pd.to_datetime(df['dteday'])
    # Tambahkan kolom baru untuk analisis waktu
    df['hour'] = df['hr']
    df['month'] = df['dteday'].dt.month
    df['day_of_week'] = df['dteday'].dt.dayofweek
    return df

df = load_data()

# Ringkasan Data
st.header(' Ringkasan Dataset')
st.write(df.describe())

# Analisis Waktu Paling Sibuk
st.header(' Waktu Paling Sibuk untuk Penyewaan')

# Tab untuk berbagai analisis waktu
tab1, tab2, tab3 = st.tabs(["Per Jam", "Per Hari", "Per Bulan"])

with tab1:
    # Analisis per jam
    hourly_rentals = df.groupby('hour')['cnt_day'].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=hourly_rentals.index, y=hourly_rentals.values, marker='o')
    plt.title('Rata-rata Penyewaan Sepeda per Jam')
    plt.xlabel('Jam')
    plt.ylabel('Rata-rata Penyewaan')
    st.pyplot(fig)
    
    # Tampilkan jam tersibuk
    peak_hour = hourly_rentals.idxmax()
    st.write(f"Jam tersibuk adalah pukul {peak_hour}:00 dengan rata-rata {hourly_rentals[peak_hour]:.0f} penyewaan")

with tab2:
    # Analisis per hari
    daily_rentals = df.groupby('day_of_week')['cnt_day'].mean()
    days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=days, y=daily_rentals.values)
    plt.title('Rata-rata Penyewaan Sepeda per Hari')
    plt.xticks(rotation=45)
    st.pyplot(fig)

with tab3:
    # Analisis per bulan
    monthly_rentals = df.groupby('month')['cnt_day'].mean()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des']
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=months, y=monthly_rentals.values)
    plt.title('Rata-rata Penyewaan Sepeda per Bulan')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Analisis Pengaruh Cuaca
st.header(' Pengaruh Cuaca terhadap Penyewaan')

# Mapping untuk label cuaca
weather_labels = {
    1: 'Cerah',
    2: 'Berawan',
    3: 'Hujan Ringan',
    4: 'Hujan Lebat'
}

# Konversi nilai weathersit ke label
df['weather_label'] = df['weathersit_day'].map(weather_labels)

# Visualisasi pengaruh cuaca
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='weather_label', y='cnt_day', data=df)
plt.title('Distribusi Penyewaan Sepeda Berdasarkan Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Jumlah Penyewaan')
st.pyplot(fig)

# Analisis Korelasi
st.header(' Korelasi Antar Jam Dengan Penyewaan')

# Hitung korelasi
correlation = df[['temp_hour', 'hum_hour', 'windspeed_hour', 'cnt_hour']].corr()

# Visualisasi korelasi dengan heatmap
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
plt.title('Matriks Korelasi Variabel Numerik')
st.pyplot(fig)

# Tambahkan metrics summary
st.header(' Ringkasan Metrik (Hour)')
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Penyewaan", f"{df['cnt_hour'].sum():,}")
with col2:
    st.metric("Rata-rata Harian", f"{df['cnt_hour'].mean():.0f}")
with col3:
    st.metric("Penyewaan Tertinggi", f"{df['cnt_hour'].max():,}")
    
    
st.header(' Korelasi Peminjaman Dengan Hari Libur')

# Hitung korelasi
correlation = df[['temp_day', 'hum_day', 'windspeed_day', 'cnt_day']].corr()

# Visualisasi korelasi dengan heatmap
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
plt.title('Matriks Korelasi Variabel Numerik')
st.pyplot(fig)

# Tambahkan metrics summary
st.header(' Ringkasan Metrik ')
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Penyewaan", f"{df['cnt_day'].sum():,}")
with col2:
    st.metric("Rata-rata Harian", f"{df['cnt_day'].mean():.0f}")
with col3:
    st.metric("Penyewaan Tertinggi", f"{df['cnt_day'].max():,}")


# Rekomendasi Berdasarkan Analisis
st.header('🎯 Rekomendasi')

# Buat columns untuk rekomendasi
col1, col2 = st.columns(2)

with col1:
    st.subheader("Waktu Terbaik untuk Penyewaan")
    st.write("""
    - Jam tersibuk adalah pukul 17:00-18:00 (jam pulang kerja)
    - Hari kerja (Senin-Jumat) memiliki penyewaan lebih tinggi
    - Musim panas (Juni-September) adalah bulan tersibuk
    """)
    
    # Visualisasi peak hours
    peak_hours = df.groupby('hour')['cnt_hour'].mean()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(x=peak_hours.index, y=peak_hours.values)
    plt.title('Peak Hours untuk Penyewaan')
    plt.xlabel('Jam')
    plt.ylabel('Rata-rata Penyewaan')
    st.pyplot(fig)

with col2:
    st.subheader("Faktor yang Mempengaruhi Penyewaan")
    st.write("""
    - Cuaca cerah dan berawan ideal untuk penyewaan
    - Suhu berkorelasi positif dengan jumlah penyewaan
    - Kelembaban dan kecepatan angin berkorelasi negatif
    - Hari kerja memiliki pola penyewaan yang lebih stabil
    """)
    
    # Visualisasi pengaruh cuaca
    weather_avg = df.groupby('weather_label')['cnt_day'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    weather_avg.plot(kind='bar')
    plt.title('Rata-rata Penyewaan Berdasarkan Cuaca')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Kesimpulan utama
st.subheader("💡 Kesimpulan Utama")
st.write("""
1. Optimalkan persediaan sepeda pada jam sibuk (17:00-18:00)
2. Tingkatkan layanan pada hari kerja dan musim panas
3. Siapkan strategi khusus untuk kondisi cuaca buruk
4. Pertimbangkan penambahan sepeda pada lokasi strategis dekat perkantoran
""")