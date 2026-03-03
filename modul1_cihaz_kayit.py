# modul1_cihaz_kayit.py
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime
import os
import subprocess
import sys

class CihazKayitModulu:
    def __init__(self, root):
        self.root = root
        self.root.title("MODÜL 1 - CİHAZ KAYIT EKRANI")
        self.root.geometry("800x850")
        
        # Excel dosya yolu
        self.dosya_yolu = "veri/cihazlar.xlsx"
        
        # Ana frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        baslik = tk.Label(main_frame, 
                         text="📝 YENİ CİHAZ KAYDI",
                         font=('Arial', 20, 'bold'),
                         fg='#27ae60')
        baslik.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Form çerçevesi
        form_frame = ttk.LabelFrame(main_frame, text="Cihaz Bilgileri", padding="15")
        form_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Satır 1: Arıza No
        ttk.Label(form_frame, text="Arıza No:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=8)
        self.ariza_no = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        self.ariza_no.grid(row=0, column=1, pady=8, padx=10)
        
        # Satır 2: Marka
        ttk.Label(form_frame, text="Marka:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=8)
        self.marka = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        self.marka.grid(row=1, column=1, pady=8, padx=10)
        
        # Satır 3: Model
        ttk.Label(form_frame, text="Model:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=8)
        self.model = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        self.model.grid(row=2, column=1, pady=8, padx=10)
        
        # Satır 4: Bölüm
        ttk.Label(form_frame, text="Bölüm:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=8)
        self.bolum = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        self.bolum.grid(row=3, column=1, pady=8, padx=10)
        
        # Satır 5: Seri No
        ttk.Label(form_frame, text="Seri No:", font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=8)
        self.seri_no = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        self.seri_no.grid(row=4, column=1, pady=8, padx=10)
        
        # Satır 6: Demirbaş No
        ttk.Label(form_frame, text="Demirbaş No:", font=('Arial', 10, 'bold')).grid(row=5, column=0, sticky=tk.W, pady=8)
        self.demirbas_no = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        self.demirbas_no.grid(row=5, column=1, pady=8, padx=10)
        
        # Satır 7: İşlem Tipi (Checkbox)
        ttk.Label(form_frame, text="İşlem Tipi:", font=('Arial', 10, 'bold')).grid(row=6, column=0, sticky=tk.W, pady=8)
        
        checkbox_frame = ttk.Frame(form_frame)
        checkbox_frame.grid(row=6, column=1, sticky=tk.W, pady=8)
        
        self.rapor_var = tk.BooleanVar()
        self.parca_var = tk.BooleanVar()
        
        ttk.Checkbutton(checkbox_frame, text="Rapor Yazıldı", 
                       variable=self.rapor_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(checkbox_frame, text="Parça İstendi", 
                       variable=self.parca_var).pack(side=tk.LEFT, padx=5)
        
        # Satır 8: Parça Bilgisi
        ttk.Label(form_frame, text="Parça Bilgisi:", font=('Arial', 10, 'bold')).grid(row=7, column=0, sticky=tk.W, pady=8)
        self.parca_bilgisi = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        self.parca_bilgisi.grid(row=7, column=1, pady=8, padx=10)
        
        # Satır 9: Son Durum
        ttk.Label(form_frame, text="Son Durum:", font=('Arial', 10, 'bold')).grid(row=8, column=0, sticky=tk.W, pady=8)
        
        self.son_durum = ttk.Combobox(form_frame, width=38, font=('Arial', 10), state='readonly')
        self.son_durum['values'] = (
            'Arıza Tespit Aşamasında',
            'Parça Bekleniyor',
            'Firmaya Gönderildi',
            'Firmadan Geldi',
            'Bölüme Teslim Edildi',
            'Tamir Edildi',
            'Hurda'
        )
        self.son_durum.grid(row=8, column=1, pady=8, padx=10)
        
        # Satır 10: Firmaya Gidiş Tarihi
        ttk.Label(form_frame, text="Firmaya Gidiş:", font=('Arial', 10, 'bold')).grid(row=9, column=0, sticky=tk.W, pady=8)
        self.firmaya_gidis = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        self.firmaya_gidis.grid(row=9, column=1, pady=8, padx=10)
        self.firmaya_gidis.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Satır 11: Firmadan Geliş
        ttk.Label(form_frame, text="Firmadan Geliş:", font=('Arial', 10, 'bold')).grid(row=10, column=0, sticky=tk.W, pady=8)
        self.firmadan_gelis = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        self.firmadan_gelis.grid(row=10, column=1, pady=8, padx=10)
        
        # Satır 12: Bölüme Teslim
        ttk.Label(form_frame, text="Bölüme Teslim:", font=('Arial', 10, 'bold')).grid(row=11, column=0, sticky=tk.W, pady=8)
        self.bolume_teslim = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        self.bolume_teslim.grid(row=11, column=1, pady=8, padx=10)
        
        # Satır 13: Notlar
        ttk.Label(form_frame, text="Notlar:", font=('Arial', 10, 'bold')).grid(row=12, column=0, sticky=tk.W, pady=8)
        self.notlar = tk.Text(form_frame, width=30, height=3, font=('Arial', 10))
        self.notlar.grid(row=12, column=1, pady=8, padx=10)
        
        # Butonlar
        buton_frame = ttk.Frame(main_frame)
        buton_frame.grid(row=2, column=0, columnspan=2, pady=30)
        
        ttk.Button(buton_frame, text="💾 KAYDET", 
                  command=self.kaydet,
                  width=15).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(buton_frame, text="🔄 TEMİZLE", 
                  command=self.temizle,
                  width=15).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(buton_frame, text="📋 CİHAZ LİSTELE", 
                  command=self.liste_modulune_git,
                  width=15).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(buton_frame, text="🏠 ANA MENÜ", 
                  command=self.ana_menu_don,
                  width=15).pack(side=tk.LEFT, padx=10)
        
        # Durum çubuğu
        self.durum = ttk.Label(main_frame, text="✅ Hazır", relief=tk.SUNKEN, anchor=tk.W)
        self.durum.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
    
    def kaydet(self):
        """Cihaz bilgilerini kaydet"""
        try:
            # Gerekli alanları kontrol et
            if not self.ariza_no.get() or not self.marka.get() or not self.model.get():
                messagebox.showwarning("Uyarı", "Lütfen zorunlu alanları doldurun!\n(Arıza No, Marka, Model)")
                return
            
            # Checkbox durumuna göre parça/rapor bilgisi
            if self.rapor_var.get() and self.parca_var.get():
                parca_rapor = "Rapor + Parça"
            elif self.rapor_var.get():
                parca_rapor = "Sadece Rapor"
            elif self.parca_var.get():
                parca_rapor = "Parça İstendi"
            else:
                parca_rapor = "Belirtilmemiş"
            
            # Yeni kayıt
            yeni_kayit = {
                "Arıza No": self.ariza_no.get(),
                "Marka": self.marka.get(),
                "Model": self.model.get(),
                "Bölüm": self.bolum.get(),
                "Seri No": self.seri_no.get(),
                "Demirbaş No": self.demirbas_no.get(),
                "İşlem Tipi": parca_rapor,
                "Parça Bilgisi": self.parca_bilgisi.get(),
                "Son Durum": self.son_durum.get(),
                "Firmaya Gidiş": self.firmaya_gidis.get(),
                "Firmadan Geliş": self.firmadan_gelis.get(),
                "Bölüme Teslim": self.bolume_teslim.get(),
                "Notlar": self.notlar.get("1.0", tk.END).strip(),
                "Kayıt Tarihi": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Son Güncelleme": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            # Excel'e kaydet
            if os.path.exists(self.dosya_yolu):
                df_mevcut = pd.read_excel(self.dosya_yolu)
                df_yeni = pd.DataFrame([yeni_kayit])
                df = pd.concat([df_mevcut, df_yeni], ignore_index=True)
            else:
                df = pd.DataFrame([yeni_kayit])
            
            df.to_excel(self.dosya_yolu, index=False)
            
            self.durum.config(text=f"✅ Kayıt başarıyla eklendi! - {datetime.now().strftime('%H:%M:%S')}")
            messagebox.showinfo("Başarılı", "Cihaz kaydı oluşturuldu!")
            self.temizle()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Kayıt eklenirken hata oluştu:\n{str(e)}")
            self.durum.config(text="❌ Kayıt hatası!")
    
    def temizle(self):
        """Formu temizle"""
        self.ariza_no.delete(0, tk.END)
        self.marka.delete(0, tk.END)
        self.model.delete(0, tk.END)
        self.bolum.delete(0, tk.END)
        self.seri_no.delete(0, tk.END)
        self.demirbas_no.delete(0, tk.END)
        self.rapor_var.set(False)
        self.parca_var.set(False)
        self.parca_bilgisi.delete(0, tk.END)
        self.son_durum.set('')
        self.firmaya_gidis.delete(0, tk.END)
        self.firmaya_gidis.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.firmadan_gelis.delete(0, tk.END)
        self.bolume_teslim.delete(0, tk.END)
        self.notlar.delete("1.0", tk.END)
        self.durum.config(text="✅ Form temizlendi")
    
    def liste_modulune_git(self):
        """Doğrudan 2. modüle git (liste ekranı)"""
        self.root.destroy()
        subprocess.Popen([sys.executable, "modul2_cihaz_liste.py"])
    
    def ana_menu_don(self):
        """Ana menüye dön"""
        self.root.destroy()
        subprocess.Popen([sys.executable, "main.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = CihazKayitModulu(root)
    root.mainloop()