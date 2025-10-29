import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import datetime

def organize_files():
    try:
        source_folder = filedialog.askdirectory(title="Pilih Folder Sumber")
        if not source_folder:
            return
        
        destination_folder = filedialog.askdirectory(title="Pilih Folder Tujuan")
        if not destination_folder:
            return
        
        # PERBAIKAN 1: Cek jika folder sumber dan tujuan sama
        if source_folder == destination_folder:
            messagebox.showwarning("Peringatan", "Folder sumber dan tujuan tidak boleh sama.")
            return

        files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
        total_files = len(files)
        
        if total_files == 0:
            messagebox.showinfo("Info", "Tidak ada file untuk dipindahkan.")
            return
        
        # Reset progress bar
        progress_bar['value'] = 0
        progress_bar['maximum'] = total_files
        root.update_idletasks()

        log_entries = []
        count_success = 0
        count_failed = 0

        for idx, filename in enumerate(files, start=1):
            try:
                file_path = os.path.join(source_folder, filename)
                
                # PERBAIKAN 2: Logika ekstensi yang lebih aman
                file_name_only, ext_with_dot = os.path.splitext(filename)
                
                if not ext_with_dot:
                    ext = "(Tanpa Ekstensi)" # Folder khusus untuk file tanpa ekstensi
                else:
                    ext = ext_with_dot[1:].lower() # Hapus titik di depan
                
                target_dir = os.path.join(destination_folder, ext)
                os.makedirs(target_dir, exist_ok=True)
                
                # PERBAIKAN 3: Mencegah overwrite/kehilangan data
                target_file_path = os.path.join(target_dir, filename)
                
                count = 1
                # Cek jika file sudah ada, ubah nama jika perlu
                while os.path.exists(target_file_path):
                    new_filename = f"{file_name_only} ({count}){ext_with_dot}"
                    target_file_path = os.path.join(target_dir, new_filename)
                    count += 1
                
                # Gunakan path file target yang sudah aman (mungkin nama baru)
                shutil.move(file_path, target_file_path)
                
                # Catat nama file *setelah* diubah (jika diubah)
                final_filename = os.path.basename(target_file_path)
                log_entries.append(f"[OK] {filename} → {target_dir}{os.sep}{final_filename}")
                count_success += 1
                
            except Exception as e:
                log_entries.append(f"[FAIL] {filename} ({e})")
                count_failed += 1
            
            # Update progress bar
            progress_bar['value'] = idx
            root.update_idletasks()
        
        # Simpan log ke file
        log_filename = os.path.join(destination_folder, f"organizer_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(log_filename, "w", encoding="utf-8") as log_file:
            log_file.write("\n".join(log_entries))
        
        # Tampilkan hasil
        messagebox.showinfo("Selesai ✅",
                            f"Berhasil: {count_success}\nGagal: {count_failed}\n\nLog tersimpan di:\n{log_filename}")

    except Exception as e:
        messagebox.showerror("Gagal ❌", f"Terjadi kesalahan:\n{e}")

# === GUI ===
root = tk.Tk()
root.title("File Organizer Otomatis (v2)")
root.geometry("400x250")
root.resizable(False, False)

label = tk.Label(root, text="Atur file berdasarkan jenisnya 📁", font=("Segoe UI", 11))
label.pack(pady=20)

btn_start = tk.Button(root, text="Mulai Atur File", command=organize_files, bg="#4CAF50", fg="white", font=("Segoe UI", 10), width=20)
btn_start.pack(pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

btn_exit = tk.Button(root, text="Keluar", command=root.quit, bg="#f44336", fg="white", font=("Segoe UI", 10), width=20)
btn_exit.pack(pady=10)

root.mainloop()
                  
