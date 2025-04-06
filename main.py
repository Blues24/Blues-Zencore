import os
import pyfiglet
from backup.fuzzer import find_folders, fuzzy_select
from backup.compress import compress_Music
from backup.upload import upload_drive
from backup.utils import print_info, print_error, print_success, print_warning


def Banner():
    fig = Figlet(font=`slant`)
    print_info(f.renderText("Blues Zencore"))

def main():
    # Clear the terminal
    os.system("clear")
    Banner()

    print_info("Mencari folder Music dan backups di rumah kamu")
    music_dirs = find_folders("/home", "Music")
    backup_dirs = find_folders("/home", "Backups")
    
    if not music_dirs:
        print_error("Folder Music tidak ditemukan")
        return
    if not backup_dirs:
        print_error("Folder Backups tidak ditemukan")
        return 
    
    source_dir, backup_dir = fuzzy_select(music_dirs, backup_dirs)

    # Config state file 
    state_file = os.path.expanduser("~/.config/blues_zencore/backup_state.json")
    
    compress_Music(source_dir, backup_dir, state_file)

if __name__ == "__main__":
    main()
