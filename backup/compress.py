import os
import tarfile
import time
import json 
import subprocess
from datetime import datetime
from backup.fuzzer import get_all_files
from backup.utils import print_info, print_error
from tqdm import tqdm

STATE_JSON = os.path.expanduser("~/.config/music_backup_state.json")

def load_backup_state():
    if os.path.exists(STATE_JSON):
        with open(STATE_JSON, "r") as file:
            return json.load(file)
    return {}

def save_backup_state(state):
    os.makedirs(os.path.dirname(STATE_JSON), exist_ok=True)
    with open(STATE_JSON, "w") as file:
        json.dump(state, file)

def modify_files(source_Dir, previous_State):
    modified = []
    current_state = {}

    for file_path in get_all_files(source_Dir):
        try:
            mtime = int(os.path.getmtime(file_path))
            current_state[file_path] = mtime
            if file_path not in previous_State or previous_State[file_path] != mtime:
                modified.append(file_path)
        except FileNotFoundError:
            continue
        
        return modified, current_state
    
def compress_Music(source_Dir, destination_Dir):
    print_info("Mengecek file yang berubah sejak backup terakhir...")
    
    previous_state = load_backup_state()
    modified_files, new_state = modify_files(source_Dir, previous_state)
    
    if not modified_files:
        print_info("✅ Tidak ada perubahan. Backup dilewati")
        return 

    # Metadata untuk nama arsip
    timestamp = datetime.now().strftime("%dd%mm%YY_%HH%MM%SS")
    archive_name = f"Blues_music_backup_{timestamp}.tar"
    backup_path = os.path.join(destination_Dir, archive_name)
    zst_path = f"{archive_name}.zst"
    
    print_info(f"📦 Mengarsipkan {len(modified_files)} file ke: {backup_path}")

    try:
        with tarfile.open(backup_path, "w") as tar:
            for file_path in tqdm(modified_files, desc="📁 Menambahkan", unit="file", dynamic_ncols=True):
                arcname = os.path.relpath(file_path, start=os.path.dirname(source_Dir))
                tar.add(file_path, arcname=arcname)
                time.sleep(0.005)
        print_info("⚙️ Mengompresi ke format .zst...")
        subprocess.run(["zstd", "--rm", backup_path], check=True)
        save_backup_state(new_state)
        print_info(f"✅ Backup selesai dan disimpan di: {zst_path}")
    except Exception as e:
        print_error(f"[!] Gagal saat backup: {e}")
