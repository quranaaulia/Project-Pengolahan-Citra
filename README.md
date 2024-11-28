# Project-Pengolahan-Citra
Aplikasi ini adalah sebuah **platform berbasis Streamlit** untuk melakukan berbagai operasi pengolahan citra secara interaktif. Berikut adalah deskripsi fitur utama dan fungsionalitas:

### **1. Fitur Utama:**
- **Input Gambar:**
  - Pengguna dapat mengunggah gambar dari perangkat (format: JPG, PNG, JPEG).
  - Alternatif: mengambil gambar langsung melalui kamera perangkat.

- **Operasi Pengolahan Citra:**
  Aplikasi menawarkan berbagai opsi pengolahan citra yang dapat dipilih melalui sidebar, yaitu:
  - **Citra Negatif:** Membalikkan nilai piksel sehingga menghasilkan versi negatif dari gambar.
  - **Grayscale:** Mengubah gambar berwarna menjadi hitam putih (grayscale).
  - **Rotasi:** Memutar gambar sebesar 90°, 180°, atau 270°.
  - **Histogram Equalization:** Meningkatkan kontras gambar menggunakan histogram equalization.
  - **Black & White:** Mengonversi gambar grayscale menjadi gambar hitam-putih berdasarkan ambang batas (threshold) yang dapat disesuaikan.
  - **Smoothing (Gaussian Blur):** Menerapkan efek blur (Gaussian) dengan radius yang dapat disesuaikan.
  - **Channel RGB:** Menampilkan hanya satu saluran warna (Red, Green, atau Blue) dari gambar berwarna.

- **Visualisasi Histogram:**
  - Menampilkan histogram dari gambar asli maupun hasil pengolahan, baik untuk gambar grayscale maupun RGB.
  - Histogram memberikan informasi distribusi intensitas piksel.

- **Hasil yang Dapat Diunduh:**
  - Hasil pengolahan gambar dapat diunduh dalam format yang sama dengan gambar asli.
  - Nama file otomatis diubah sesuai dengan jenis pengolahan yang dilakukan.

### **2. Antarmuka dan Tampilan:**
- Menggunakan **CSS kustom** untuk mengatur estetika aplikasi, termasuk:
  - Sidebar dan navigasi dengan latar belakang warna magenta tua (#740938).
  - Latar belakang aplikasi utama dengan warna merah jambu (#C71585).

- **Interaktivitas:**
  - Sidebar sebagai kontrol utama untuk memilih metode input, jenis pengolahan citra, dan parameter tambahan (seperti threshold atau rotasi).
  - Layout responsif dengan pembagian kolom untuk menampilkan gambar dan histogram secara berdampingan.

### **3. Teknologi yang Digunakan:**
- **Streamlit:** Untuk antarmuka aplikasi berbasis web.
- **Pillow (PIL):** Untuk manipulasi gambar.
- **NumPy:** Untuk pengolahan data numerik pada citra.
- **Matplotlib:** Untuk visualisasi histogram.
- **BytesIO:** Untuk mengonversi gambar hasil pengolahan ke format unduh.

### **Alur Penggunaan:**
1. **Input Gambar:**
   - Unggah file atau ambil foto langsung.
   - Gambar yang diunggah akan ditampilkan di halaman utama.

2. **Pilih Mode Pengolahan:**
   - Pilih salah satu metode dari daftar opsi di sidebar.
   - Sesuaikan parameter jika diperlukan (misalnya: threshold untuk Black & White).

3. **Lihat Hasil:**
   - Hasil pengolahan gambar akan ditampilkan bersama histogramnya.
   - Gambar asli juga tersedia untuk perbandingan.

4. **Unduh Hasil:**
   - Klik tombol **Download** untuk menyimpan hasil ke perangkat.

### **Tujuan Aplikasi:**
Aplikasi ini ditujukan untuk:
- Mempermudah eksplorasi dan eksperimen pengolahan citra secara interaktif.
- Memberikan cara sederhana bagi pengguna umum atau pelajar untuk memahami konsep dasar dalam pengolahan gambar, seperti histogram equalization, filter Gaussian, dan channel RGB.
