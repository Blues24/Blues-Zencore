from Zencore.utils import ConsoleTemplate 
from Zencore.compress import Archiver
from Zencore.fuzzer import Fuzzer
from Zencore.createPassword import Security, Checker
from InquirerPy import inquirer
import argparse
import os, sys

def get_args():
    parser = argparse.ArgumentParser(description="Blues Zencore - Backup utility")
    parser.add_argument("source", nargs="?", help="Folder yang ingin di-backup")
    parser.add_argument("destination", nargs="?", help="Folder tujuan backup")
    return parser.parse_args()

def select_folder_path(name: str, target: str):
    
    all_path = Fuzzer.find_target_folder(os.path.expanduser("~"), target)
    if not all_path:
        ConsoleTemplate.print_error(f"Sorry, folder not found!")
        sys.exit(1)
    
    return inquirer.fuzzy(
        message=f"choose a folder for {name}",
        choices=all_path
    ).execute()

def main():
    ConsoleTemplate.show_banner()
    args = get_args()

    source = args.source if args.source and os.path.isdir(args.source) else Fuzzer.fuzzy_select("source", "Music")
    destination = args.destination if args.destination and os.path.isdir(args.destination) else Fuzzer.fuzzy_select("tujuan", "Backups")

    archive_name = inquirer.text(message="📝 Nama arsip backup:").execute()
    algorithm = inquirer.select(
        message="📦 Pilih algoritma kompresi:",
        choices=["tar.zst", "tar.gz", "zip", "7z"]
    ).execute()

    use_password = inquirer.confirm(message="🔐 Apakah ingin mengenkripsi arsip dengan password?", default=False).execute()
    password = None
    if use_password:
        password = inquirer.secret(message="Masukkan password:").execute()

    # get all file within the target directory
    
    file_list = Fuzzer.get_all_files(source)

    if not file_list:
        ConsoleTemplate.print_warning("Tidak ada file yang ditemukan untuk dibackup.")
        return

    # 📦 COMPRESS
    compressor = Archiver(source, destination, archive_name, algorithm)
    archive_path = compressor.get_archive_path()
    # 🔐 ENCRYPT
    if use_password:
        encryptor = Security(password)
        encryptor.encrypt_file(archive_path)

    # ✅ VERIFY didn't work because didn't generate original hashhhh
    #verifier = Checker()
    #verifier.verify_hash(archive_path)

    ConsoleTemplate.thank_you()


if __name__ == "__main__":
    main()