# main.py
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

class AnaProgram:
    def __init__(self, root):
        self.root = root
        self.root.title("CİHAZ TAKİP SİSTEMİ - ANA MENÜ")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        # Arka plan rengi
        self.root.configure(bg='#2c3e50')
        
        # Başlık
        baslik_frame = tk.Frame(root, bg='#34495e', height=100)
        baslik_frame.pack(fill=tk.X)
        
        baslik = tk.Label(baslik_frame, 
                         text="🏥 HASTANE CİHAZ TAKİP SİSTEMİ",
                         font=('Arial', 18, 'bold'),
                         bg='#34495e',
                         fg='white')
        baslik.pack(expand=True, pady=30)
        
        # İSİM EKLENDİ
        isim_label = tk.Label(baslik_frame,
                             text="Gökalp YATIKKAYA",
                             font=('Arial', 12, 'italic'),
                             bg='#34495e',
                             fg='#ecf0f1')
        isim_label.pack(pady=(0, 10))
        
        # Butonlar için frame
        buton_frame = tk.Frame(root, bg='#2c3e50')
        buton_frame.pack(expand=True)
        
        # Modül 1 Butonu - Cihaz Kayıt
        self.modul1_buton = tk.Button(buton_frame,
                                     text="📝 1. MODÜL\nCİHAZ KAYIT",
                                     font=('Arial', 14, 'bold'),
                                     bg='#27ae60',
                                     fg='white',
                                     width=20,
                                     height=3,
                                     cursor='hand2',
                                     command=self.modul1_ac)
        self.modul1_buton.pack(pady=20)
        
        # Modül 2 Butonu - Cihaz Listele
        self.modul2_buton = tk.Button(buton_frame,
                                     text="📋 2. MODÜL\nCİHAZ LİSTELE",
                                     font=('Arial', 14, 'bold'),
                                     bg='#2980b9',
                                     fg='white',
                                     width=20,
                                     height=3,
                                     cursor='hand2',
                                     command=self.modul2_ac)
        self.modul2_buton.pack(pady=20)
        
        # Çıkış Butonu
        cikis_buton = tk.Button(buton_frame,
                               text="❌ ÇIKIŞ",
                               font=('Arial', 12),
                               bg='#c0392b',
                               fg='white',
                               width=15,
                               height=1,
                               cursor='hand2',
                               command=self.cikis)
        cikis_buton.pack(pady=30)
        
        # Alt bilgi - İSİM EKLENDİ
        alt_bilgi = tk.Label(root,
                            text="v1.0 - Hastane Cihaz Takip Sistemi | Gökalp YATIKKAYA",
                            font=('Arial', 9),
                            bg='#2c3e50',
                            fg='#7f8c8d')
        alt_bilgi.pack(side=tk.BOTTOM, pady=10)
        
        # Veri klasörünü kontrol et
        if not os.path.exists("veri"):
            os.makedirs("veri")
    
    def modul1_ac(self):
        """1. Modülü aç (Cihaz Kayıt)"""
        try:
            self.root.destroy()
            subprocess.Popen([sys.executable, "modul1_cihaz_kayit.py"])
        except Exception as e:
            messagebox.showerror("Hata", f"Modül açılamadı:\n{str(e)}")
    
    def modul2_ac(self):
        """2. Modülü aç (Cihaz Listele)"""
        try:
            self.root.destroy()
            subprocess.Popen([sys.executable, "modul2_cihaz_liste.py"])
        except Exception as e:
            messagebox.showerror("Hata", f"Modül açılamadı:\n{str(e)}")
    
    def cikis(self):
        """Programdan çık"""
        if messagebox.askyesno("Çıkış", "Programdan çıkmak istediğinizden emin misiniz?"):
            self.root.quit()
            self.root.destroy()
            sys.exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnaProgram(root)
    root.mainloop()