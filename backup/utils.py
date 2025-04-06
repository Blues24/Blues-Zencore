from colorama import Fore, Style, init 

# Memulai colorama
init(autoreset=True)

# Untuk debug info 
def print_info(text):
    print(Fore.CYAN + "[*] " + Style.BRIGHT + text)

# Untuk debug proses yang sukses
def print_success(text):
    print(Fore.GREEN + "[✓] " + Style.BRIGHT + text)

# Untuk debug proses yang error
def print_error(text):
    print(Fore.RED + "[!] " + Style.BRIGHT + text)

# Untuk print peringatan
def print_warning(text):
    print(Fore.YELLOW + "[!] " + Style.BRIGHT + text)
