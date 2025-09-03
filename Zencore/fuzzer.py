import os 
from InquirerPy import inquirer as search
from Zencore.utils import ConsoleTemplate

class Fuzzer:
    def fuzzy_select(options, prompt_title):
        if not options:
            ConsoleTemplate.print_warning(f"[{prompt_title}] Tidak ada yang cocok")
            return None 

        if len(options) == 1:
            ConsoleTemplate.print_info(f"Otomatis memilih opsi: {options[0]}")
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
        ConsoleTemplate.print_info("🔍 Mencari folder Music dan Backups...")

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
