import os
import json
import hashlib

def _get_folder_hash(folder):
    hash_sha256 = hashlib.sha256()
    for root, _, files in os.walk(folder):
        for name in sorted(files):  # urutkan agar konsisten
            path = os.path.join(root, name)
            try:
                with open(path, 'rb') as f:
                    while chunk := f.read(8192):
                        hash_sha256.update(chunk)
            except Exception:
                continue
    return hash_sha256.hexdigest()

def has_changed_since_last_backup(folder, state_file):
    new_hash = _get_folder_hash(folder)

    if not os.path.exists(state_file):
        return True

    with open(state_file, 'r') as f:
        state = json.load(f)

    return state.get('hash') != new_hash

def save_state(folder, state_file):
    folder_hash = _get_folder_hash(folder)
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    with open(state_file, 'w') as f:
        json.dump({'hash': folder_hash}, f)

