from colorama import Fore, Style, init
import pyfiglet
from tqdm import tqdm
import sys
import time

init(autoreset=True)

class ConsoleTemplate:
    @staticmethod
    def print_info(message):
        print(f"{Fore.CYAN}[•] {message}{Style.RESET_ALL}")

    @staticmethod
    def print_success(message):
        print(f"{Fore.GREEN}[✓] {message}{Style.RESET_ALL}")

    @staticmethod
    def print_warning(message):
        print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")

    @staticmethod
    def print_error(message):
        print(f"{Fore.RED}[X] {message}{Style.RESET_ALL}")

    @staticmethod
    def show_banner():
        banner = pyfiglet.figlet_format("Blues Zencore")
        print(f"{Fore.MAGENTA}{banner}{Style.RESET_ALL}")

    @staticmethod
    def thank_you():
        print(f"{Fore.GREEN}Terimakasih telah memakai program ini!{Style.RESET_ALL}")

    @staticmethod
    def loading_bar(task_name, total_steps):
        with tqdm(total=total_steps, desc=task_name, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as bar:
            for _ in range(total_steps):
                time.sleep(0.1)  # Simulasi loading
                bar.update(1)
