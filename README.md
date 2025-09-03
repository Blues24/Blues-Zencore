# 🎶 Blues Zencore

**Blues Zencore** adalah tool backup musik minimalis dan interaktif berbasis Python.  
Dibuat untuk pengguna Linux yang ingin menyimpan koleksi musik mereka secara efisien dan aman dengan:

- 🔍 Fuzzy Finder Folder `Music/` dan `Backups/`
- 📦 Format backup `.tar.zst` seperti sistem paket Arch
- 🔐 Verifikasi SHA-256 otomatis
- 🎛️ CLI interaktif dengan animasi progress bar
- 📅 Penjadwalan dengan `systemd-timer` (opsional)
- 💬 Notifikasi CLI berwarna dengan `colorama`
**Sekarang masih belum work di windows karena saya tidak punya windows hehehe**
---

## 📦 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/Blues24/Blues-Zencore.git
cd blues-zencore

2. Install Dependensi Python

Disarankan menggunakan virtualenv atau venv

pip install -r requirements.txt

3. Install Dependency Sistem

Blues Zencore memerlukan beberapa paket dari sistem:
Debian/Ubuntu:

sudo apt install zstd fzf

Arch/Manjaro:

sudo pacman -S zstd fzf python-colorama python-tqdm python-pyfiglet

Fedora/Nobara:

sudo dnf install zstd fzf

🚀 Menjalankan Backup

python -m blues_zencore

Lalu ikuti prompt interaktif:

    Pilih folder Music

    Pilih folder tujuan Backups

    Backup akan dikompresi & diverifikasi

📅 Menambahkan Pengingat Manual (Opsional)

Buat script pengingat untuk backup rutin (jika tidak pakai systemd-timer):

bash reminder.sh

📁 Struktur Direktori

blues_zencore/
│
├── main.py                 # Entry point
├── compress.py             # Backup & kompresi + checksum
├── finder.py               # Fuzzy folder finder
├── utils.py                # Output helper
├── requirements.txt        # Dependency Python
└── README.md

⚙️ Todo dan Fitur Mendatang

    🔁 Restore system backup (WIP)

    ☁️ Upload ke Google Drive (WIP)

    🔔 Notifikasi via desktop (WIP)

📜 Lisensi

Blues Zencore menggunakan lisensi GPL.

