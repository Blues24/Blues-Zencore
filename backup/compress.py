import os
import tarfile
import time
import json 
import subprocess
import hashlib
from datetime import datetime
from backup.fuzzer import get_all_files
from backup.utils import print_info, print_error, print_success, print_warning
from backup.state import has_changed_since_last_backup, save_state
from tqdm import tqdm

def generate_checksum(file_path):
    sha256checksum = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256checksum.update(chunk)
    return sha256checksum.hexdigest()

def save_checksum_file(file_path, checksum):
    checksum_path = file_path + ".sha256"
    with open(checksum_path, "w") as f:
        f.write(f"{checksum} {os.path.basename(file_path)}\n")
    return checksum_path

def verify_checksum(file_path, expected_checksum):
    actual_checksum = generate_checksum(file_path)
    return actual_checksum == expected_checksum

def compress_Music(source_Dir, destination_Dir, state_file):
    if not os.path.isdir(source_Dir):
        print_error("Folder sumber tidak valid.")
        return

    if not os.path.isdir(destination_Dir):
        print_error("Folder backup tidak valid")
        return

    # Cek apakah ada perubahan file dari backup sebelumnya ada atau tidak ada 
    if not has_changed_since_last_backup(source_Dir, state_file):
        backup_name = f"{datetime.now().strftime(`%dd%mm%YY_%HH_%MM%SS`)}_Music_Backup.tar.zst"
        backup_path = os.path.join(destination_Dir, backup_name)
        if os.path.exists(backup_path):
            print_info("Tidak ada perubahan sejak backup terakhir. Lewati backup.")
            return

        print_info("Menyiapkan pembuatan arsip")

        all_files = get_all_files(source_Dir)
        total_files = len(all_files)
        backup_name = f"{datetime.now().strftime(`%dd%mm%YY_%HH%MM%SS`)}_Music_Backup.tar.zst"
        output_path = os.path.join(destination_Dir, backup_name)

        try:
            with tarfile.open(output_path, "w|") as tar, tqdm(total=total_files, desc="📦 Mengarsip", unit="file") as pbar:
                for file_path in all_files:
                    arcname = os.path.relpath(file_path, source_Dir)
                    tar.add(file_path, arcname=arcname)
                    pbar.update(1)

            # Kompress lagi dengan zstd 
            os.system(f"zstd --rm {output_path}")

            # Tambahkan arsip .zst ke path baru 
            zst_path = output_path + ".zst"

            # Buat checksum dan simpan checksum
            checksum = generate_checksum(zst_path)
            save_checksum_file(zst_path, checksum)

            print_success(f"[✓] SHA-256 Arsip: {checksum}")
            if verify_checksum(zst_path, checksum):
                print_success("[✓] Verifikasi checksum berhasil!")
            else:
                print_warning("[!] Verifikasi checksum GAGAL!")

            save_state(source_Dir, state_file)
            print_success("Backup selesasi dan state tersimpan.")
        except Exception as e:
            print_error(f"Gagal saat pembuatan arsip karena: {e}")

