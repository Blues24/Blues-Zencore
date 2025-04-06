import os
import pyfiglet
from backup.fuzzer import find_folders
from backup.compress import compress_Music
from backup.upload import upload_drive
from backup.utils import print_info, print_error, print_success

def main():
    # Clear the terminal
    os.system("clear")

    # Make the banner
    banner = pyfiglet.figlet_format("Blues Backup script", font="slant")
    print(banner)
    
    folders = find_folders()
    if not folders:
        return
    
    compress_Music(folders["music"], folders["backups"])

if __name__ == "__main__":
    main()
