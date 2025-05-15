import os
import tarfile
import subprocess
import zipfile
import zstandard as zstd 
from Zencore.utils import ConsoleTemplate

class Archiver:
     def __init__(self, source, destination, archive_name, algorithm):
        self.source = source
        self.destination = destination
        self.archive_name = archive_name
        self.algorithm = algorithm.lower()
        self.supported_algorithms = ["tar.gz", "tar.zst", "zip"]
        self.archive_path = os.path.join(destination, f"{archive_name}.{self._get_extension()}")  # path disimpan
        self.compress()
     def compress(self):
        archive_path = os.path.join(self.destination, f"{self.archive_name}.{self._get_extension()}")
        ConsoleTemplate.print_info(f"Menggunakan algoritma kompresi: {self.algorithm}")
        if self.algorithm == "tar.gz":
            self._compress_tar_gz(self.source, archive_path)
        elif self.algorithm == "tar.zst":
            self._compress_tar_zst(self.source, archive_path)
        elif self.algorithm == "zip":
            self._compress_zip(self.source, archive_path)
        else:
            ConsoleTemplate.print_error(f"Algoritma tidak didukung: {self.algorithm}")
            raise ValueError(f"Unsupported compression algorithm: {self.algorithm}")
        return archive_path

     def _compress_tar_gz(self, source_path, archive_path):
        with tarfile.open(archive_path, "w:gz") as tar:
            for root, _, files in os.walk(source_path):
                for file in ConsoleTemplate.loading_bar("GZIP Compressing", files):
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, start=source_path)
                    tar.add(full_path, arcname=arcname)

     def _compress_tar_zst(self, source_path, archive_path):
        cctx = zstd.ZstdCompressor()
        with open(archive_path, "wb") as zst_file:
            with cctx.stream_writer(zst_file) as compressor:
                with tarfile.open(fileobj=compressor, mode="w|") as tar:
                    for root, _, files in os.walk(source_path):
                        for file in ConsoleTemplate.loading_bar("ZSTD Compressing", files):
                            full_path = os.path.join(root, file)
                            arcname = os.path.relpath(full_path, start=source_path)
                            tar.add(full_path, arcname=arcname)

     def _compress_zip(self, source_path, archive_path):
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(source_path):
                for file in ConsoleTemplate.loading_bar("ZIP Compressing", files):
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, start=source_path)
                    zipf.write(full_path, arcname=arcname)

     def _get_extension(self):
        if self.algorithm == "tar.gz":
            return "tar.gz"
        elif self.algorithm == "tar.zst":
            return "tar.zst"
        elif self.algorithm == "zip":
            return "zip"
        else:
            return "archive"
     def get_archive_path(self):
        return self.archive_path        
