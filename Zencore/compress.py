import os
import tarfile
import subprocess
import zipfile
import hashlib
import zstandard as zstd

from datetime import datetime
from Zencore.utils import Logger as log, LoadingTime  # Comming soon


class Compressor:
    def __init__(self, source_folder: str, destination_folder: str, algorithm: str):
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.algorithm = algorithm
        self.archive_path = None
        self.checksum = None

    def generate_archive(self):
        base = os.path.basename(os.path.abspath(self.source_folder))
        timestamp_data = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = {
            "tar.zst": ".tar.zst",
            "zip": ".zip",
            "tar.gz": ".tar.gz",
            "7zip": ".7z"
        }.get(self.algorithm, ".archive")
        self.archive_path = os.path.join(
            self.destination_folder, base + "_", + timestamp_data, + ext)

    def compress(self):
        self.generate_archive()
        log.info(f"mengompress {self.source_folder} ke {
                 self.archive_path} menggunakan {self.algorithm}")

        if self.algorithm == "tar.zst":
            self._compress_zstd()
        elif self.algorithm == "tar.gz":
            self._compress_gzip()
        elif self.algorithm == "zip":
            self._zip()
        elif self.algorithm == "7zip":
            self._compress_7zip()
        else:
            log.error("Tidak dapat menemukan algorithma yang kamu mau")
            return

        self.generate_checksum()

    def _compress_zstd(self):
        cctx = zstd.ZstdCompressor()
        with open(self.archive_path, "wb") as f_out:
            with cctx.stream_writer(f_out) as compressor:
                with tarfile.open(fileobj=compressor, mode="w|") as tar:
                    total_files = sum(
                        [len(files)
                            for _, _, files in os.walk(self.source_folder)])
                    loadingBar = LoadingTime.create_bar(total_files,
                                                        desc="📦 Mengarsipkan",
                                                        ncols=70,
                                                        unit="file")
                    for root, _, files in os.walk(self.source_folder):

                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(
                                file_path, self.source_folder)

                            try:
                                tar.add(file_path, arcname=arcname)
                            except Exception as err:
                                log.warning(f"Gagal menambahkan {
                                            file_path}: {err}")

                            loadingBar.update(1)
                    loadingBar.close()
                log.success("Berhasil membuat arsip dengan zstandard")

    def _zip(self):
        with zipfile.ZipFile(self.archive_path, "w", zipfile.ZIP_DEFLATED) as zipfw:
            total_files = sum([len(files) for _, _, files in os.walk(self.source_folder)])
            bar = LoadingTime.create_bar(total_files, desc="📦 Mengarsipkan", ncols=70, unit="file")
            for root, _, files in os.walk(self.source_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.source_folder)
                    try:
                        zipfw.write(file_path, arcname)
                    except Exception as e:
                        log.warning(f"Gagal menambahkan {file_path}: {e}")
                    bar.update(1)
            bar.close()
    def _compress_7zip(self):
        log.info("Menggunakan algoritma 7z")
        command = ["7z", "a", self.archive_path, self.source_folder]
        try:
            subprocess.run(command, check=True)
            log.success("Kompresi dengan 7z selesai.")
        except FileNotFoundError:
            log.error(
                "Perintah '7z' tidak ditemukan. Pastikan 7zip telah terinstal.")
        except subprocess.CalledProcessError as e:
            log.error(f"Gagal menjalankan 7z: {e}")

    def generate_checksum(self):
        sha256_hash = hashlib.sha256()
        try:
            with open(self.archive_path, "rb") as fw:
                for chunk in iter(lambda: fw.read(4096), b""):
                    sha256_hash.update(chunk)
                self.checksum = sha256_hash.hexdigest()
                log.success(f"Berhasil membuat checksum SHA256: {
                            self.checksum}")
        except Exception as err:
            log.error(f"Gagal membuat checksum karena: {err}")

    def run(self):
        self.compress()
        return self.archive_path, self.checksum
