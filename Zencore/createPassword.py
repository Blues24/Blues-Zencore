import hashlib
from cryptography.fernet import Fernet, InvalidToken
from Zencore.utils import ConsoleTemplate
import os

class Security:
    def __init__(self, password: str):
        self.key = self.derive_key(password)
    def derive_key(self, password: str) -> bytes:
        # encode base64 into fernet key
        import base64
        return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
    
    def encrypt_file(self, file_path: str) -> str:
        fernet = Fernet(self.key)
        with open(file_path, "rb") as fileRead:
            encrypted = fernet.encrypt(fileRead.read())
        
        backup_path = f"file_path.bak"
        os.rename(file_path, backup_path)
        
        with open(encrypted_path, "wb") as fileWrite:
            fileWrite.write(encrypted)
        
        ConsoleTemplate.print_success(f"The file has been encrypted")
        return file_path
    
    def decrypt_file(self, file_path: str) -> str:
        fernet = Fernet(self.key)

        with open(file_path, 'rb') as file:
            decrypted = fernet.decrypt(file.read())

        with open(file_path, 'wb') as file:
            file.write(decrypted)

        ConsoleTemplate.success(f"File didekripsi: {file_path}")
        return file_path

class Checker:
    def __init__(self):
        self.hash = None
        self.original_hash = None

    def generate_hash(self, file_path: str) -> str:
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as Read:
            for chunk in iter(lambda: Read.read(4096), 'b'):
                sha256.update(chunk)
        self.hash =  sha256.hexdigest()
        self.original_hash = self.hash
        ConsoleTemplate.print_info(f"Archive original checksum: {self.hash} in sha256 algorithm")
        
    def verify_hash(self, file_path: str,) -> bool:
        current_hash = self.generate_hash(file_path)
        is_valid = current_hash == original_hash
        if is_valid:
            ConsoleTemplate.print_success("Valid Checksum")
        else:
            ConsoleTemplate.print_error("Invalid Checksum")
        return is_valid