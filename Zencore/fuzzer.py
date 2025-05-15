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
