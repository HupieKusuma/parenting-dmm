# Parenting DMM

Parenting DMM adalah aplikasi web berbasis Flask yang memungkinkan orang tua untuk memantau data akademik siswa.  
Sistem ini menggunakan Google Sheets sebagai database utama dan menyediakan akses terhadap nilai ujian, progres hafalan, serta informasi silabus.

---

## Gambaran Umum

Proyek ini dirancang untuk lingkungan pendidikan skala kecil seperti pondok pesantren.  
sistem ini terintegrasi dengan Google Sheets melalui service account untuk mengelola dan mengambil data siswa.

Aplikasi ini ringan, mudah dideploy, dan sederhana dalam perawatan.

---

## Fitur

- Login siswa menggunakan ID dan nama  
- Dashboard yang menampilkan:
  - Nilai ujian  
  - Progres hafalan  
  - Informasi kelas  
- Halaman silabus berdasarkan kelas siswa  
- Autentikasi berbasis session  
- Google Sheets sebagai backend database  

---

## Teknologi yang Digunakan

- Python 3.9+
- Flask
- gspread (Google Sheets API)
- Jinja2
- HTML / CSS

---

## Struktur Proyek

```
parenting-dmm/
├── app.py
├── sheets.py
├── requirements.txt
├── templates/
└── static/
```

- `app.py` – Aplikasi Flask utama dan routing  
- `sheets.py` – Logika integrasi Google Sheets  
- `templates/` – Template HTML (Jinja2)  
- `static/` – File CSS dan aset statis  

---

## Instalasi

### 1. Clone repository

```bash
git clone https://github.com/HupieKusuma/parenting-dmm
cd parenting-dmm
```

### 2. Install dependency

```bash
pip install -r requirements.txt
```

---

## Konfigurasi Google Sheets

Proyek ini menggunakan Google Sheets sebagai database.

Langkah yang perlu dilakukan:

1. Buat service account di Google Cloud.
2. Aktifkan Google Sheets API dan Google Drive API.
3. Unduh file kredensial service account (`credentials.json`).
4. Bagikan spreadsheet Anda ke email service account tersebut.

### Worksheet yang Dibutuhkan

Spreadsheet harus memiliki worksheet berikut:

- `students`
- `exam_scores`
- `hafalan`
- `silabus_jadwal`

Pastikan struktur kolom sesuai dengan yang dibutuhkan oleh backend.

---

## Menjalankan Aplikasi

```bash
python app.py
```

Secara default aplikasi berjalan di:

```
http://localhost:8000
```

---

## Cara Kerja Sistem

- Login memvalidasi ID dan nama siswa dari sheet `students`.
- Setelah autentikasi berhasil, sistem mengambil:
  - Data nilai ujian  
  - Data hafalan  
  - Informasi kelas  
- Data ditampilkan menggunakan template Flask.
- Terdapat caching sederhana untuk mengurangi jumlah request ke Google Sheets API.

---


All rights reserved.
This project may not be copied, modified, or distributed without explicit permission from the author.
