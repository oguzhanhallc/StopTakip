import tkinter as tk
from tkinter import ttk, messagebox

class Urun:
    def __init__(self, ad, stok):
        self.ad = ad
        self.stok = stok

    def stok_guncelle(self, miktar):
        self.stok += miktar

class Siparis:
    siparis_sayaci = 1
    def __init__(self, urun, miktar):
        self.siparis_no = Siparis.siparis_sayaci
        Siparis.siparis_sayaci += 1
        self.urun = urun
        self.miktar = miktar

    def __str__(self):
        return f"Sipariş #{self.siparis_no} - {self.urun.ad}: {self.miktar} adet"

class StokTakipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stok Takip Sistemi")
        self.root.geometry("700x400")
        self.root.configure(bg="#d9f2d9")

        self.urunler = []
        self.siparisler = []

        ttk.Label(root, text="📦 Stok Takip Sistemi", font=("Segoe UI", 18, "bold")).pack(pady=10)

        urun_frame = ttk.LabelFrame(root, text="Ürün Ekleme", padding=10)
        urun_frame.pack(pady=10, fill="x", padx=10)

        ttk.Label(urun_frame, text="Ürün Adı:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.urun_ad_entry = ttk.Entry(urun_frame, width=30)
        self.urun_ad_entry.grid(row=0, column=1, pady=5)

        ttk.Label(urun_frame, text="Stok Miktarı:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.stok_miktar_entry = ttk.Entry(urun_frame, width=30)
        self.stok_miktar_entry.grid(row=1, column=1, pady=5)

        ttk.Button(urun_frame, text="Ürün Ekle", command=self.urun_ekle).grid(row=2, column=0, columnspan=2, pady=10)

        siparis_frame = ttk.LabelFrame(root, text="Sipariş Oluştur", padding=10)
        siparis_frame.pack(pady=10, fill="x", padx=10)

        ttk.Label(siparis_frame, text="Ürün Seç:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.urun_sec_combo = ttk.Combobox(siparis_frame, values=[], state="readonly", width=28)
        self.urun_sec_combo.grid(row=0, column=1, pady=5)

        ttk.Label(siparis_frame, text="Sipariş Miktarı:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.siparis_miktar_entry = ttk.Entry(siparis_frame, width=30)
        self.siparis_miktar_entry.grid(row=1, column=1, pady=5)

        ttk.Button(siparis_frame, text="Sipariş Ver", command=self.siparis_ver).grid(row=2, column=0, columnspan=2, pady=10)

        # Yeni frame: yan yana liste için
        liste_frame = ttk.Frame(root)
        liste_frame.pack(pady=10, fill="both", expand=True, padx=10)

        # Mevcut stoklar ve siparişler yan yana
        stok_frame = ttk.Frame(liste_frame)
        stok_frame.pack(side="left", fill="both", expand=True, padx=(0,5))

        siparis_frame2 = ttk.Frame(liste_frame)
        siparis_frame2.pack(side="right", fill="both", expand=True, padx=(5,0))

        ttk.Label(stok_frame, text="Mevcut Stoklar:", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.stok_listbox = tk.Listbox(stok_frame, height=15)
        self.stok_listbox.pack(fill="both", expand=True, pady=5)

        ttk.Label(siparis_frame2, text="Verilen Siparişler:", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.siparis_listbox = tk.Listbox(siparis_frame2, height=15)
        self.siparis_listbox.pack(fill="both", expand=True, pady=5)

        # Güncelle ve Sil butonları siparişler altına
        ttk.Button(siparis_frame2, text="Siparişi Güncelle", command=self.siparis_guncelle).pack(pady=(5,2), fill="x")
        ttk.Button(siparis_frame2, text="Siparişi İptal Et", command=self.siparis_iptal).pack(pady=(0,5), fill="x")

        # Sipariş seçildiğinde bilgi alanlarını doldur
        self.siparis_listbox.bind("<<ListboxSelect>>", self.siparis_secildi)

    def urun_ekle(self):
        ad = self.urun_ad_entry.get().strip()
        stok_str = self.stok_miktar_entry.get().strip()

        if not ad or not stok_str:
            messagebox.showwarning("Hata", "Ürün adı ve stok miktarını girin!")
            return
        try:
            stok = int(stok_str)
            if stok < 0:
                raise ValueError
        except:
            messagebox.showwarning("Hata", "Stok miktarı sıfır veya pozitif tam sayı olmalı!")
            return

        for u in self.urunler:
            if u.ad.lower() == ad.lower():
                messagebox.showwarning("Hata", "Bu isimde ürün zaten var!")
                return

        yeni_urun = Urun(ad, stok)
        self.urunler.append(yeni_urun)

        self.guncelle_urun_combobox()
        self.guncelle_stok_listesi()

        messagebox.showinfo("Başarılı", f"Ürün '{ad}' eklendi.")

        self.urun_ad_entry.delete(0, tk.END)
        self.stok_miktar_entry.delete(0, tk.END)

    def guncelle_urun_combobox(self):
        isimler = [u.ad for u in self.urunler]
        self.urun_sec_combo['values'] = isimler
        if isimler:
            self.urun_sec_combo.current(0)

    def siparis_ver(self):
        secili_urun_ad = self.urun_sec_combo.get()
        miktar_str = self.siparis_miktar_entry.get().strip()

        if not secili_urun_ad:
            messagebox.showwarning("Hata", "Lütfen bir ürün seçin!")
            return
        if not miktar_str:
            messagebox.showwarning("Hata", "Sipariş miktarını girin!")
            return

        try:
            miktar = int(miktar_str)
            if miktar <= 0:
                raise ValueError
        except:
            messagebox.showwarning("Hata", "Sipariş miktarı pozitif tam sayı olmalı!")
            return

        urun = next((u for u in self.urunler if u.ad == secili_urun_ad), None)
        if urun is None:
            messagebox.showerror("Hata", "Seçilen ürün bulunamadı!")
            return

        if urun.stok < miktar:
            messagebox.showwarning("Hata", f"Yetersiz stok! Mevcut stok: {urun.stok}")
            return

        urun.stok_guncelle(-miktar)
        yeni_siparis = Siparis(urun, miktar)
        self.siparisler.append(yeni_siparis)

        self.guncelle_stok_listesi()
        self.guncelle_siparis_listesi()

        messagebox.showinfo("Başarılı", f"{miktar} adet '{urun.ad}' siparişi verildi.")

        self.siparis_miktar_entry.delete(0, tk.END)

    def guncelle_stok_listesi(self):
        self.stok_listbox.delete(0, tk.END)
        for u in self.urunler:
            self.stok_listbox.insert(tk.END, f"{u.ad} - Stok: {u.stok}")

    def guncelle_siparis_listesi(self):
        self.siparis_listbox.delete(0, tk.END)
        for s in self.siparisler:
            self.siparis_listbox.insert(tk.END, str(s))

    def siparis_secildi(self, event):
        secim = self.siparis_listbox.curselection()
        if not secim:
            return
        index = secim[0]
        siparis = self.siparisler[index]
        try:
            urun_index = [u.ad for u in self.urunler].index(siparis.urun.ad)
            self.urun_sec_combo.current(urun_index)
        except ValueError:
            pass
        self.siparis_miktar_entry.delete(0, tk.END)
        self.siparis_miktar_entry.insert(0, str(siparis.miktar))

    def siparis_guncelle(self):
        secim = self.siparis_listbox.curselection()
        if not secim:
            messagebox.showwarning("Uyarı", "Güncellenecek siparişi seçin.")
            return

        index = secim[0]
        siparis = self.siparisler[index]

        secili_urun_ad = self.urun_sec_combo.get()
        miktar_str = self.siparis_miktar_entry.get().strip()

        if not secili_urun_ad:
            messagebox.showwarning("Hata", "Lütfen bir ürün seçin!")
            return
        if not miktar_str:
            messagebox.showwarning("Hata", "Sipariş miktarını girin!")
            return

        try:
            yeni_miktar = int(miktar_str)
            if yeni_miktar <= 0:
                raise ValueError
        except:
            messagebox.showwarning("Hata", "Sipariş miktarı pozitif tam sayı olmalı!")
            return

        yeni_urun = next((u for u in self.urunler if u.ad == secili_urun_ad), None)
        if yeni_urun is None:
            messagebox.showerror("Hata", "Seçilen ürün bulunamadı!")
            return

        # Eski siparişteki ürünün stoğunu geri ekle
        siparis.urun.stok_guncelle(siparis.miktar)

        # Yeni sipariş için stok kontrolü
        if yeni_urun.stok < yeni_miktar:
            # Önce eski stoğu geri düşür (iptal)
            siparis.urun.stok_guncelle(-siparis.miktar)
            messagebox.showwarning("Hata", f"Yetersiz stok! Mevcut stok: {yeni_urun.stok}")
            return

        # Siparişi güncelle
        siparis.urun = yeni_urun
        siparis.miktar = yeni_miktar

        # Yeni siparişin stoğunu düş
        yeni_urun.stok_guncelle(-yeni_miktar)

        self.guncelle_stok_listesi()
        self.guncelle_siparis_listesi()

        messagebox.showinfo("Başarılı", "Sipariş güncellendi.")

    def siparis_iptal(self):
        secim = self.siparis_listbox.curselection()
        if not secim:
            messagebox.showwarning("Uyarı", "İptal edilecek siparişi seçin.")
            return

        index = secim[0]
        siparis = self.siparisler.pop(index)

        # Stokları geri ekle
        siparis.urun.stok_guncelle(siparis.miktar)

        self.guncelle_stok_listesi()
        self.guncelle_siparis_listesi()

        messagebox.showinfo("Başarılı", "Sipariş iptal edildi.")

        # Temizle giriş alanları
        self.siparis_miktar_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = StokTakipApp(root)
    root.mainloop()
