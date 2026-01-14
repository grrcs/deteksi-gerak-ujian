# 👁️ Deteksi Gerak Ujian (Exam Proctoring System)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Detection-orange?style=for-the-badge)

## 📋 Tentang Proyek

**Deteksi Gerak Ujian** adalah sistem pengawasan otomatis berbasis *Computer Vision* yang dirancang untuk menjaga integritas ujian online. Sistem ini menggunakan webcam untuk memantau perilaku peserta secara *real-time* dan mendeteksi indikasi kecurangan melalui analisis gerak dan orientasi wajah.

Aplikasi ini bertujuan untuk membantu pengawas ujian dengan memberikan notifikasi otomatis jika peserta melakukan gerakan mencurigakan, seperti menoleh terlalu lama atau meninggalkan tempat duduk.

## ✨ Fitur Utama

* **Head Pose Estimation:** Mendeteksi arah pandangan kepala (Kiri, Kanan, Atas, Bawah) untuk mengetahui jika peserta melihat contekan.
* **Face Presence Detection:** Memastikan wajah peserta selalu terlihat di depan layar.
* **Multiple Face Detection:** Memberikan peringatan jika terdeteksi lebih dari satu wajah dalam satu frame.
* **Real-time Alert:** Menampilkan peringatan visual di layar saat terjadi pelanggaran.
* **Activity Logging (Opsional):** Mencatat waktu dan jenis pelanggaran yang terdeteksi.

## 🛠️ Teknologi yang Digunakan

* **Python 3.x**: Bahasa pemrograman utama.
* **OpenCV**: Untuk pengolahan citra dan akses kamera.
* **MediaPipe**: Untuk ekstraksi *landmark* wajah yang presisi dan ringan.
* **NumPy**: Untuk perhitungan geometri dan matematika.

## 🚀 Cara Instalasi

Ikuti langkah-langkah berikut untuk menjalankan proyek ini di komputer Anda:

1.  **Clone Repository**
    ```bash
    git clone [https://github.com/](https://github.com/)[username-anda]/deteksi-gerak-ujian.git
    cd deteksi-gerak-ujian
    ```

2.  **Install Dependencies**
    Pastikan Python sudah terinstal, lalu jalankan:
    ```bash
    pip install opencv-python mediapipe numpy
    ```

3.  **Jalankan Aplikasi**
    ```bash
    python main.py
    ```

## 🎮 Cara Penggunaan

1.  Pastikan webcam terhubung dan berfungsi.
2.  Jalankan script `main.py`.
3.  Jendela kamera akan terbuka.
4.  Sistem akan mulai mendeteksi wajah Anda:
    * **Status Aman:** Jika Anda menatap lurus ke layar.
    * **Peringatan:** Jika Anda menoleh ke kiri/kanan/atas/bawah melebihi sudut toleransi.
5.  Tekan tombol `q` pada keyboard untuk keluar dari aplikasi.

## 📂 Struktur Folder

```text
deteksi-gerak-ujian/
│
├── main.py            # Kode utama aplikasi
├── utils.py           # Fungsi bantuan (hitung sudut, dll)
├── requirements.txt   # Daftar library yang dibutuhkan
└── README.md          # Dokumentasi proyek
```
📸 Screenshot
![WhatsApp Image 2026-01-14 at 10 50 24](https://github.com/user-attachments/assets/776e4549-95be-4174-bc6f-5003379cfe26)

