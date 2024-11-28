import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import numpy as np
from matplotlib import pyplot as plt
import os
from io import BytesIO

# Konfigurasi halaman
st.set_page_config(page_title="PengolahanCitra", page_icon="📸")

# Pengaturan tampilan sidebar dan header aplikasi menggunakan CSS
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #740938;
        }
        [data-testid="stSidebarNav"] {
            background-color: #740938;
        }
        .css-1d391kg {
            background-color: #740938;
        }
        /* Background color */
        .stApp {
            background-color: #C71585;
        }

    </style>
""", unsafe_allow_html=True)


# Fungsi untuk menampilkan gambar dengan judul
def tampilkan_judul(citra, judul):
    st.image(citra, caption=judul, use_container_width=True)

def tampilkan_histogram(citra):
    fig, ax = plt.subplots(figsize=(8, 5))  # Menambahkan ukuran figur yang lebih besar
    
    # Memeriksa apakah citra berwarna (RGB) atau grayscale
    if len(citra.shape) == 3:  # Histogram untuk gambar berwarna
        color = ('r', 'g', 'b')  # Warna saluran RGB
        labels = ('Red', 'Green', 'Blue')
        
        # Hitung jumlah pixel non-zero untuk setiap channel
        non_zero_channels = np.sum(citra != 0, axis=(0,1))
        
        # Jika hanya satu channel yang memiliki nilai (channel RGB mode)
        if np.count_nonzero(non_zero_channels) == 1:
            # Temukan channel yang aktif
            active_channel = np.argmax(non_zero_channels)
            # Plot hanya channel yang aktif
            hist = np.histogram(citra[:, :, active_channel], bins=256, range=(0, 256))[0]
            ax.bar(np.arange(256), hist, color=color[active_channel], alpha=0.7, width=1.5, edgecolor='darkgray', linewidth=1)
            ax.set_title(f'Histogram ({labels[active_channel]} Channel)')
        else:
            # Plot semua channel untuk gambar RGB normal
            for i, (col, label) in enumerate(zip(color, labels)):
                hist = np.histogram(citra[:, :, i], bins=256, range=(0, 256))[0]
                ax.bar(np.arange(256), hist, color=col, alpha=0.5, width=1.5, edgecolor='darkgray', linewidth=1, label=label)
            ax.set_title('Histogram (RGB)')
    else:  # Histogram untuk gambar grayscale
        hist, _ = np.histogram(citra.flatten(), bins=256, range=(0, 256))
        ax.bar(np.arange(256), hist, color='black', alpha=0.7, width=1.5, edgecolor='darkgray', linewidth=1)
        ax.set_title('Histogram (Grayscale)')
    
    ax.set_xlim([0, 256])
    ax.set_xlabel('Pixel Value')
    ax.set_ylabel('Frequency')
    ax.legend()
    plt.tight_layout()  # Menyesuaikan tata letak plot
    st.pyplot(fig)

# Fungsi untuk mengkonversi array numpy menjadi bytes
def convert_image_to_bytes(image_array):
    img = Image.fromarray(image_array.astype(np.uint8))
    buf = BytesIO()
    img.save(buf, format='PNG')
    byte_im = buf.getvalue()
    return byte_im

# Judul Aplikasi
st.title("Pengolahan Citra")

# Tambahkan pilihan input di sidebar
st.sidebar.title("Input Gambar")
input_method = st.sidebar.radio("Pilih Metode Input", ["Upload File", "Kamera"])

if input_method == "Upload File":
    uploaded_file = st.file_uploader("Upload gambar yuk!", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        img_np = np.array(img)
        use_image = True
else:
    # Fitur kamera
    camera_image = st.camera_input("Ambil Foto")
    if camera_image is not None:
        img = Image.open(camera_image)
        img = img.transpose(Image.FLIP_LEFT_RIGHT)  # Membalik gambar secara horizontal untuk menghilangkan efek mirror
        img_np = np.array(img)
        use_image = True
    else:
        use_image = False

# Pemrosesan gambar jika ada input
if 'use_image' in locals() and use_image:
    # Menampilkan gambar dan histogram asli
    st.subheader("Gambar Asli dan Histogram")
    col1, col2 = st.columns(2)
    with col1:
        tampilkan_judul(img_np, "Gambar Asli")
    with col2:
        tampilkan_histogram(img_np)

    # Sidebar untuk memilih mode pemrosesan gambar
    st.sidebar.subheader("Pilih Mode Pengolahan Citra")
    opsi = st.sidebar.selectbox("Mode Pengolahan", (
        "Citra Negatif", "Grayscale", "Rotasi", 
        "Histogram Equalization", "Black & White", "Smoothing (Gaussian Blur)", "Channel RGB"
    ))

    # Input untuk threshold jika opsi "Black & White" dipilih
    if opsi == "Black & White":
        threshold = st.sidebar.number_input("Threshold Level", min_value=0, max_value=255, value=127)

    # Button untuk memilih derajat rotasi jika opsi "Rotasi" dipilih
    if opsi == "Rotasi":
        rotasi = st.sidebar.radio("Pilih Derajat Rotasi", (90, 180, 270))

    # Field input untuk blur radius jika opsi "Smoothing (Gaussian Blur)" dipilih
    if opsi == "Smoothing (Gaussian Blur)":
        blur_radius = st.sidebar.text_input("Masukkan Blur Radius", value="10")
        try:
            blur_radius = float(blur_radius)
        except ValueError:
            st.sidebar.error("Masukkan nilai numerik yang valid untuk blur radius.")
            blur_radius = 10  # Default value jika input salah

    # Pilihan channel jika opsi "Channel RGB" dipilih
    if opsi == "Channel RGB":
        channel = st.sidebar.selectbox("Pilih Channel", ("Red", "Green", "Blue"))

    # Fungsi untuk mengolah gambar berdasarkan opsi
    def olah_gambar(img_np, opsi):
        if opsi == "Citra Negatif":
            return np.clip(255 - img_np.astype(np.uint8), 0, 255)
        
        elif opsi == "Grayscale":
            return np.array(ImageOps.grayscale(Image.fromarray(img_np.astype(np.uint8))))
        
        elif opsi == "Rotasi":
            if rotasi == 90:
                return np.rot90(img_np, 1)
            elif rotasi == 180:
                return np.rot90(img_np, 2)
            elif rotasi == 270:
                return np.rot90(img_np, 3)
            
        elif opsi == "Histogram Equalization":
            img_rgb = Image.fromarray(img_np.astype(np.uint8))
            r, g, b = img_rgb.split()
            r_eq = ImageOps.equalize(r)
            g_eq = ImageOps.equalize(g)
            b_eq = ImageOps.equalize(b)
            img_eq = Image.merge("RGB", (r_eq, g_eq, b_eq))
            return np.array(img_eq)
        
        elif opsi == "Black & White":
            gray = np.array(ImageOps.grayscale(Image.fromarray(img_np.astype(np.uint8))))
            bw = np.where(gray > threshold, 255, 0).astype(np.uint8)
            return bw
        
        elif opsi == "Smoothing (Gaussian Blur)":
            return np.array(Image.fromarray(img_np.astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=blur_radius)))
        
        elif opsi == "Channel RGB":
            img_channel = np.zeros_like(img_np)
            channel_map = {"Red": 0, "Green": 1, "Blue": 2}
            img_channel[:, :, channel_map[channel]] = img_np[:, :, channel_map[channel]]
            return img_channel

    # Pemrosesan gambar berdasarkan opsi
    hasil = olah_gambar(img_np, opsi)

    # Menampilkan hasil pemrosesan dan histogram
    st.subheader(f"Hasil - {opsi}")
    col1, col2 = st.columns(2)
    with col1:
        tampilkan_judul(hasil, f"Hasil - {opsi}")
    with col2:
        tampilkan_histogram(hasil)

    # Membuat nama file untuk hasil yang akan diunduh
    if input_method == "Upload File":
        original_filename = uploaded_file.name
    else:
        original_filename = "camera_capture.jpg"
    
    ext = os.path.splitext(original_filename)[1]
    nama_file_simpan = f"{os.path.splitext(original_filename)[0]}-{opsi.lower().replace(' ', '_')}{ext}"

    # Konversi hasil menjadi bytes
    hasil_bytes = convert_image_to_bytes(hasil)

    # Tombol download
    st.download_button(
        label=f"Download {opsi}",
        data=hasil_bytes,
        file_name=nama_file_simpan,
        mime=f"image/{ext[1:]}"
    )

else:
    if input_method == "Upload File":
        st.write("Silakan upload gambar terlebih dahulu ya.")
    else:
        st.write("Silakan ambil foto terlebih dahulu ya.")