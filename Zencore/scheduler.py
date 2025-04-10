import os
from backup.utils import print_info, print_success, print_error

SERVICE_NAME = "music-backup.service"
TIMER_FILE = "music-backup.timer"
INSTALL_SERVICE_PATH = os.path.expanduser("~/.config/systemd/user")

def create_scheduler(script_path: str):
    try:
        os.makedirs(INSTALL_SERVICE_PATH, exists_ok=True)

        service_file = f"""[Unit]
Description=Backup Musik ke Arsip Tar.zst

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 {script_path}
"""

        timer_file = """[Unit]
Description=Jadwalkan backup musik setiap 2 bulan

[Timer]
OnCalendar=*-*/2-01 00:00:00
Persistent=true

[Install]
WantedBy=timers.target
"""
        with open(os.path.join(INSTALL_SERVICE_PATH, SERVICE_NAME), "w") as file:
            f.write(service_file)
        with open(os.path.join(INSTALL_SERVICE_PATH, TIMER_FILE), "w") as timerW:
            timerW.write(timer_file)

        # Enable dan start timer langsung
        os.system("systemctl --user daemon-reload")
        os.system("systemctl --user enable --now {TIMER_FILE}")

        print_success("Systemd timer berhasil di setup !")
        print_info("Jalankan `systemctl --user list-timers untuk melihat timer`")

    except Exception as err:
        print_error(f"Gagal menjalankan systemd timer: {err}")
