# **Panduan Menjalankan Project Python**

Agar project Python bisa dijalankan dengan lancar, kita perlu menyiapkan Python, membuat lingkungan kerja khusus (virtual environment), lalu menginstal library yang dibutuhkan. Ikuti langkah-langkah berikut:

---

### 1. Pasang Python

Pertama, pastikan Python versi **3.11.9** sudah ada di komputer.
Unduh dari sini:
👉 [https://www.python.org/downloads/release/python-3119/](https://www.python.org/downloads/release/python-3119/)

Saat instalasi, centang pilihan **Add Python to PATH** supaya Python bisa langsung dipakai di terminal.

---

### 2. Buka PowerShell

Buka aplikasi **Windows PowerShell**.

Agar nanti bisa mengaktifkan virtual environment, ada dua hal yang perlu disiapkan:

1. **Aktifkan Developer Mode** (cukup sekali saja)

   * Buka **Settings → Privacy & Security → For Developers**.
   * Hidupkan opsi **Developer Mode**.

2. **Ijinkan PowerShell menjalankan script**

   * Jalankan PowerShell **sebagai Administrator**.
   * Ketik perintah berikut:

     ```powershell
     Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```
   * Pilih `Y` (Yes) jika muncul pertanyaan.

Setelah ini, PowerShell bisa dipakai untuk mengaktifkan virtual environment.

---

### 3. Masuk ke Folder Project

Gunakan perintah ini untuk masuk ke folder project:

```powershell
cd <nama_folder_project>
```

Ganti `<nama_folder_project>` dengan lokasi folder project Anda.

---

### 4. Buat Virtual Environment

Buat lingkungan khusus untuk project dengan perintah:

```powershell
python -m venv .venv
```

---

### 5. Aktifkan Virtual Environment

Aktifkan dengan perintah:

```powershell
.\.venv\Scripts\Activate.ps1
```

Kalau berhasil, di depan baris PowerShell akan muncul tulisan `(.venv)`.

---

### 6. Pasang Library yang Dibutuhkan

Di dalam virtual environment, pasang semua library dengan perintah:

```powershell
pip install transformers[torch] accelerate hf-xet
```

---

### 7. Jalankan Program

Terakhir, jalankan file utama project dengan perintah:

```powershell
python main.py
```

Kalau semua langkah benar, program Anda akan berjalan.
