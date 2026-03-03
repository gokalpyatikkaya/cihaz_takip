# modul2_cihaz_liste.py
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime
import os
import subprocess
import sys

class CihazListeModulu:
    def __init__(self, root):
        self.root = root
        self.root.title("MODÜL 2 - CİHAZ LİSTELEME EKRANI")
        self.root.geometry("1100x800")
        
        # Excel dosya yolu
        self.dosya_yolu = "veri/cihazlar.xlsx"
        
        # Ana frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        baslik_frame = tk.Frame(main_frame, bg='#2980b9', height=60)
        baslik_frame.pack(fill=tk.X, pady=(0, 10))
        
        baslik = tk.Label(baslik_frame, 
                         text="📋 KAYITLI CİHAZLAR LİSTESİ",
                         font=('Arial', 18, 'bold'),
                         bg='#2980b9',
                         fg='white')
        baslik.pack(expand=True)
        
        # Arama çerçevesi
        arama_frame = ttk.LabelFrame(main_frame, text="Cihaz Ara", padding="10")
        arama_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(arama_frame, text="Ara:").pack(side=tk.LEFT, padx=5)
        self.arama_entry = ttk.Entry(arama_frame, width=30)
        self.arama_entry.pack(side=tk.LEFT, padx=5)
        self.arama_entry.bind('<KeyRelease>', self.arama_yap)
        
        ttk.Button(arama_frame, text="🔄 Yenile", 
                  command=self.listeyi_yenile).pack(side=tk.RIGHT, padx=5)
        
        # Liste çerçevesi
        liste_frame = ttk.Frame(main_frame)
        liste_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview (tablo) ve scrollbar
        columns = ('Arıza No', 'Marka', 'Model', 'Bölüm', 'Seri No', 'Son Durum', 'Kayıt Tarihi')
        
        # Treeview
        self.tree = ttk.Treeview(liste_frame, columns=columns, show='headings', height=20)
        
        # Scrollbar
        vsb = ttk.Scrollbar(liste_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(liste_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Kolon başlıkları
        self.tree.heading('Arıza No', text='Arıza No')
        self.tree.heading('Marka', text='Marka')
        self.tree.heading('Model', text='Model')
        self.tree.heading('Bölüm', text='Bölüm')
        self.tree.heading('Seri No', text='Seri No')
        self.tree.heading('Son Durum', text='Son Durum')
        self.tree.heading('Kayıt Tarihi', text='Kayıt Tarihi')
        
        # Kolon genişlikleri
        self.tree.column('Arıza No', width=100)
        self.tree.column('Marka', width=80)
        self.tree.column('Model', width=80)
        self.tree.column('Bölüm', width=100)
        self.tree.column('Seri No', width=100)
        self.tree.column('Son Durum', width=150)
        self.tree.column('Kayıt Tarihi', width=130)
        
        # Grid'e yerleştir
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Grid ağırlıkları
        liste_frame.grid_rowconfigure(0, weight=1)
        liste_frame.grid_columnconfigure(0, weight=1)
        
        # İstatistik çerçevesi
        istatistik_frame = ttk.LabelFrame(main_frame, text="İstatistikler", padding="10")
        istatistik_frame.pack(fill=tk.X, pady=10)
        
        self.toplam_label = ttk.Label(istatistik_frame, text="Toplam Cihaz: 0", font=('Arial', 10, 'bold'))
        self.toplam_label.pack(side=tk.LEFT, padx=20)
        
        self.durum_label = ttk.Label(istatistik_frame, text="Son Durum Dağılımı: -", font=('Arial', 10))
        self.durum_label.pack(side=tk.LEFT, padx=20)
        
        # Alt butonlar - DÜZENLE BUTONU EKLENDİ
        buton_frame = ttk.Frame(main_frame)
        buton_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(buton_frame, text="📊 Detay Göster", 
                  command=self.detay_goster).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buton_frame, text="✏️ DÜZENLE", 
                  command=self.cihaz_duzenle,
                  width=12).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buton_frame, text="📁 Excel Aç", 
                  command=self.excel_ac).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buton_frame, text="📝 CİHAZ KAYIT", 
                  command=self.kayit_modulune_git).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buton_frame, text="🏠 ANA MENÜ", 
                  command=self.ana_menu_don).pack(side=tk.RIGHT, padx=5)
        
        # Listeyi yükle
        self.listeyi_yenile()
    
    def listeyi_yenile(self):
        """Listeyi yenile"""
        # Mevcut listeyi temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if os.path.exists(self.dosya_yolu):
            try:
                df = pd.read_excel(self.dosya_yolu)
                
                # Verileri ekle
                for _, row in df.iterrows():
                    self.tree.insert('', tk.END, values=(
                        row['Arıza No'],
                        row['Marka'],
                        row['Model'],
                        row['Bölüm'],
                        row['Seri No'],
                        row['Son Durum'],
                        row['Kayıt Tarihi']
                    ))
                
                # İstatistikleri güncelle
                self.istatistikleri_guncelle(df)
                
            except Exception as e:
                messagebox.showerror("Hata", f"Liste yüklenirken hata:\n{str(e)}")
        else:
            # Boş liste mesajı
            self.tree.insert('', tk.END, values=('Henüz kayıt yok!', '', '', '', '', '', ''))
            self.toplam_label.config(text="Toplam Cihaz: 0")
            self.durum_label.config(text="Son Durum Dağılımı: -")
    
    def istatistikleri_guncelle(self, df):
        """İstatistikleri güncelle"""
        # Toplam cihaz
        toplam = len(df)
        self.toplam_label.config(text=f"Toplam Cihaz: {toplam}")
        
        # Son durum dağılımı
        if toplam > 0 and 'Son Durum' in df.columns:
            durum_sayilari = df['Son Durum'].value_counts()
            durum_text = "Son Durum: "
            for durum, sayi in durum_sayilari.head(3).items():
                durum_text += f"{durum}: {sayi}  "
            self.durum_label.config(text=durum_text)
    
    def arama_yap(self, event=None):
        """Arama yap"""
        aranan = self.arama_entry.get().lower()
        
        if not aranan:
            self.listeyi_yenile()
            return
        
        # Listeyi temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if os.path.exists(self.dosya_yolu):
            df = pd.read_excel(self.dosya_yolu)
            
            # Arama yap
            for _, row in df.iterrows():
                if (aranan in str(row['Arıza No']).lower() or
                    aranan in str(row['Marka']).lower() or
                    aranan in str(row['Model']).lower() or
                    aranan in str(row['Bölüm']).lower() or
                    aranan in str(row['Seri No']).lower()):
                    
                    self.tree.insert('', tk.END, values=(
                        row['Arıza No'],
                        row['Marka'],
                        row['Model'],
                        row['Bölüm'],
                        row['Seri No'],
                        row['Son Durum'],
                        row['Kayıt Tarihi']
                    ))
    
    def detay_goster(self):
        """Seçili cihazın detaylarını göster"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen bir cihaz seçin!")
            return
        
        # Detay penceresi
        detay_win = tk.Toplevel(self.root)
        detay_win.title("Cihaz Detayı")
        detay_win.geometry("600x500")
        
        # Seçili kaydı bul
        item = self.tree.item(selected[0])
        ariza_no = item['values'][0]
        
        df = pd.read_excel(self.dosya_yolu)
        kayit = df[df['Arıza No'] == ariza_no].iloc[0]
        
        # Detayları göster
        row = 0
        for kolon in df.columns:
            tk.Label(detay_win, text=f"{kolon}:", 
                    font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, padx=10, pady=2)
            
            # Uzun metinler için wrap
            value = str(kayit[kolon])
            if len(value) > 50:
                value = value[:50] + "..."
            
            tk.Label(detay_win, text=value, 
                    font=('Arial', 10), wraplength=350).grid(row=row, column=1, sticky=tk.W, padx=10, pady=2)
            row += 1
    
    def cihaz_duzenle(self):
        """Seçili cihazı düzenle"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen düzenlenecek cihazı seçin!")
            return
        
        # Seçili kaydı bul
        item = self.tree.item(selected[0])
        ariza_no = item['values'][0]
        
        # Excel'den kaydı al
        df = pd.read_excel(self.dosya_yolu)
        kayit = df[df['Arıza No'] == ariza_no].iloc[0]
        kayit_index = df[df['Arıza No'] == ariza_no].index[0]
        
        # Düzenleme penceresi
        duzenle_win = tk.Toplevel(self.root)
        duzenle_win.title(f"Cihaz Düzenle - {ariza_no}")
        duzenle_win.geometry("700x650")
        
        # Ana frame
        main_frame = ttk.Frame(duzenle_win, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        baslik = tk.Label(main_frame, 
                         text=f"✏️ CİHAZ DÜZENLE - {ariza_no}",
                         font=('Arial', 16, 'bold'),
                         fg='#2980b9')
        baslik.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Form çerçevesi
        form_frame = ttk.LabelFrame(main_frame, text="Cihaz Bilgileri", padding="15")
        form_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Mevcut değerlerle doldurulmuş giriş kutuları
        row = 0
        
        # Arıza No (değiştirilemez)
        ttk.Label(form_frame, text="Arıza No:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=8)
        ariza_no_label = ttk.Label(form_frame, text=str(kayit['Arıza No']), font=('Arial', 10))
        ariza_no_label.grid(row=row, column=1, sticky=tk.W, pady=8, padx=10)
        row += 1
        
        # Marka
        ttk.Label(form_frame, text="Marka:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=8)
        marka_entry = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        marka_entry.insert(0, str(kayit['Marka']))
        marka_entry.grid(row=row, column=1, pady=8, padx=10)
        row += 1
        
        # Model
        ttk.Label(form_frame, text="Model:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=8)
        model_entry = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        model_entry.insert(0, str(kayit['Model']))
        model_entry.grid(row=row, column=1, pady=8, padx=10)
        row += 1
        
        # Bölüm
        ttk.Label(form_frame, text="Bölüm:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=8)
        bolum_entry = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        bolum_entry.insert(0, str(kayit['Bölüm']))
        bolum_entry.grid(row=row, column=1, pady=8, padx=10)
        row += 1
        
        # Seri No
        ttk.Label(form_frame, text="Seri No:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=8)
        seri_no_entry = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        seri_no_entry.insert(0, str(kayit['Seri No']))
        seri_no_entry.grid(row=row, column=1, pady=8, padx=10)
        row += 1
        
        # Demirbaş No
        ttk.Label(form_frame, text="Demirbaş No:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=8)
        demirbas_entry = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        demirbas_entry.insert(0, str(kayit['Demirbaş No']))
        demirbas_entry.grid(row=row, column=1, pady=8, padx=10)
        row += 1
        
        # İşlem Tipi (Checkbox)
        ttk.Label(form_frame, text="İşlem Tipi:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=8)
        
        checkbox_frame = ttk.Frame(form_frame)
        checkbox_frame.grid(row=row, column=1, sticky=tk.W, pady=8)
        
        rapor_var = tk.BooleanVar()
        parca_var = tk.BooleanVar()
        
        # Mevcut duruma göre checkbox'ları ayarla
        islem_tipi = str(kayit['İşlem Tipi'])
        if 'Rapor' in islem_tipi:
            rapor_var.set(True)
        if 'Parça' in islem_tipi:
            parca_var.set(True)
        
        ttk.Checkbutton(checkbox_frame, text="Rapor Yazıldı", 
                       variable=rapor_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(checkbox_frame, text="Parça İstendi", 
                       variable=parca_var).pack(side=tk.LEFT, padx=5)
        row += 1
        
        # Parça Bilgisi
        ttk.Label(form_frame, text="Parça Bilgisi:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=8)
        parca_entry = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        parca_entry.insert(0, str(kayit['Parça Bilgisi']))
        parca_entry.grid(row=row, column=1, pady=8, padx=10)
        row += 1
        
        # Son Durum
        ttk.Label(form_frame, text="Son Durum:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=8)
        
        son_durum_combo = ttk.Combobox(form_frame, width=38, font=('Arial', 10), state='readonly')
        son_durum_combo['values'] = (
            'Arıza Tespit Aşamasında',
            'Parça Bekleniyor',
            'Firmaya Gönderildi',
            'Firmadan Geldi',
            'Bölüme Teslim Edildi',
            'Tamir Edildi',
            'Hurda'
        )
        son_durum_combo.set(str(kayit['Son Durum']))
        son_durum_combo.grid(row=row, column=1, pady=8, padx=10)
        row += 1
        
        # Firmaya Gidiş
        ttk.Label(form_frame, text="Firmaya Gidiş:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=8)
        firmaya_entry = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        firmaya_entry.insert(0, str(kayit['Firmaya Gidiş']))
        firmaya_entry.grid(row=row, column=1, pady=8, padx=10)
        row += 1
        
        # Firmadan Geliş
        ttk.Label(form_frame, text="Firmadan Geliş:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=8)
        firmadan_entry = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        firmadan_entry.insert(0, str(kayit['Firmadan Geliş']))
        firmadan_entry.grid(row=row, column=1, pady=8, padx=10)
        row += 1
        
        # Bölüme Teslim
        ttk.Label(form_frame, text="Bölüme Teslim:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=8)
        teslim_entry = ttk.Entry(form_frame, width=40, font=('Arial', 10))
        teslim_entry.insert(0, str(kayit['Bölüme Teslim']))
        teslim_entry.grid(row=row, column=1, pady=8, padx=10)
        row += 1
        
        # Notlar
        ttk.Label(form_frame, text="Notlar:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=8)
        notlar_text = tk.Text(form_frame, width=30, height=3, font=('Arial', 10))
        notlar_text.insert("1.0", str(kayit['Notlar']))
        notlar_text.grid(row=row, column=1, pady=8, padx=10)
        
        # Kaydet butonu
        def kaydet_degisiklikler():
            try:
                # Checkbox durumuna göre işlem tipi
                if rapor_var.get() and parca_var.get():
                    yeni_islem_tipi = "Rapor + Parça"
                elif rapor_var.get():
                    yeni_islem_tipi = "Sadece Rapor"
                elif parca_var.get():
                    yeni_islem_tipi = "Parça İstendi"
                else:
                    yeni_islem_tipi = "Belirtilmemiş"
                
                # DataFrame'i güncelle
                df.loc[kayit_index, 'Marka'] = marka_entry.get()
                df.loc[kayit_index, 'Model'] = model_entry.get()
                df.loc[kayit_index, 'Bölüm'] = bolum_entry.get()
                df.loc[kayit_index, 'Seri No'] = seri_no_entry.get()
                df.loc[kayit_index, 'Demirbaş No'] = demirbas_entry.get()
                df.loc[kayit_index, 'İşlem Tipi'] = yeni_islem_tipi
                df.loc[kayit_index, 'Parça Bilgisi'] = parca_entry.get()
                df.loc[kayit_index, 'Son Durum'] = son_durum_combo.get()
                df.loc[kayit_index, 'Firmaya Gidiş'] = firmaya_entry.get()
                df.loc[kayit_index, 'Firmadan Geliş'] = firmadan_entry.get()
                df.loc[kayit_index, 'Bölüme Teslim'] = teslim_entry.get()
                df.loc[kayit_index, 'Notlar'] = notlar_text.get("1.0", tk.END).strip()
                df.loc[kayit_index, 'Son Güncelleme'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                # Excel'e kaydet
                df.to_excel(self.dosya_yolu, index=False)
                
                messagebox.showinfo("Başarılı", "Cihaz bilgileri güncellendi!")
                duzenle_win.destroy()
                self.listeyi_yenile()  # Listeyi yenile
                
            except Exception as e:
                messagebox.showerror("Hata", f"Güncelleme sırasında hata:\n{str(e)}")
        
        # Butonlar
        buton_frame = ttk.Frame(main_frame)
        buton_frame.grid(row=2, column=0, columnspan=2, pady=30)
        
        ttk.Button(buton_frame, text="💾 KAYDET", 
                  command=kaydet_degisiklikler,
                  width=15).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(buton_frame, text="❌ İPTAL", 
                  command=duzenle_win.destroy,
                  width=15).pack(side=tk.LEFT, padx=10)
    
    def excel_ac(self):
        """Excel dosyasını aç"""
        if os.path.exists(self.dosya_yolu):
            os.startfile(self.dosya_yolu)
        else:
            messagebox.showwarning("Uyarı", "Excel dosyası bulunamadı!")
    
    def kayit_modulune_git(self):
        """Doğrudan 1. modüle git (kayıt ekranı)"""
        self.root.destroy()
        subprocess.Popen([sys.executable, "modul1_cihaz_kayit.py"])
    
    def ana_menu_don(self):
        """Ana menüye dön"""
        self.root.destroy()
        subprocess.Popen([sys.executable, "main.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = CihazListeModulu(root)
    root.mainloop()