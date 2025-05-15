<<<<<<< HEAD
import os
from InquirerPy import inquirer
from Zencore.utils import ConsoleTemplate
class Fuzzer:
    def __init__(self):
        self.console = ConsoleTemplate()
    
    def find_target(self, base_path, target_name):
        results = []
        for root, dirs, _ in os.walk(base_path):
            for d in dirs:
                if d.lower() == target_name.lower():
                    results.append(os.path.join(root, d))
        
        return results

    def get_all_files(self, folder):
        file_paths = []
        for root, _, files in os.walk(folder):
            for file in files:
                file_paths.append(os.path.join(root, file))
        
        return file_paths

    def select_folders(self, folders, message):
        if not folders:
            self.console.print_warning("I'm sorry, can't find your folders")
            
            return None
        return inquirer.fuzzy(
            message=message,
            choices=folders,
        ).execute()
=======
import os 
from InquirerPy import inquirer as search
from backup.utils import print_info, print_warning, print_error

def fuzzy_select(options, prompt_title):
    if not options:
        print_warning(f"[{prompt_title}] Tidak ada yang cocok")
        return None 

    if len(options) == 1:
        print_info(f"Otomatis memilih opsi: {options[0]}")
        return options[0]

    return search.fuzzy(
            message=f"{prompt_title}",
            choices=options,
            max_height="75%",
            default=options[0]
            ).execute()

def find_target_folder(base_path, target_name):
    result = []
    for root, dirs, _ in os.walk(base_path):
        for d in dirs:
            if d.lower() == target_name.lower():
                result.append(os.path.join(root, d))
    return result

def get_all_files(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


def find_folders(base_path="/home/blues/"):
    print_info("🔍 Mencari folder Music dan Backups...")

    music_Dir = find_target_folder(base_path, "music")
    backup_Dir = find_target_folder(base_path, "backups")

    if not music_Dir or not backup_Dir:
        print_error("❌ Tidak menemukan folder target.")
        return None 
    source_Dir = search.fuzzy(
            message="🎵 Pilih folder Music:",
            choices=music_Dir,
            max_height="70%",
    ).execute()
    destination_Dir = search.fuzzy(
            message="💾 Pilih folder Backups:",
            choices=backup_Dir,
            max_height="70%"
    ).execute()

    return {
        "music": source_Dir,
        "backups": destination_Dir
    }
>>>>>>> main
