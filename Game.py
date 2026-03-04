import json
import os
import random
import pygame
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Launcher")
        self.root.geometry("300x200")
        self.root.resizable(width=False, height=False)
        
        # Oyun İçi Değişkenler
        self.oyun_sayac = 0
        self.dogru_sayac = 0
        self.health = 2
        self.oyun_sayisi = 3
        self.musicdongu = 10
        self.oyuncu_ismi = ""
        self.frameCnt = 23
        self.hikaye_sayac = 0
        self.konusma_sayac = 0
        self.secilen_soru = None
        self.mevcut_sorular = []
        
        # Pygame Ses Sistemi
        pygame.mixer.init()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Resimleri Yükleme
        self.load_images()
        # Soruları Yükleme
        self.load_questions()
        
        # Başlangıç Arayüzü
        self.setup_launcher()
        
    def get_path(self, *paths):
        return os.path.join(self.base_dir, *paths)
        
    def load_images(self):
        try:
            self.launcher_image1 = ImageTk.PhotoImage(Image.open(self.get_path('texture', 'launcher.jpg')))
            self.story_resim1 = ImageTk.PhotoImage(Image.open(self.get_path('texture', 'doga.jpg')))
            self.katbir_resim1 = ImageTk.PhotoImage(Image.open(self.get_path('texture', 'magara.jpg')))
            self.katbir_kapiresim1 = ImageTk.PhotoImage(Image.open(self.get_path('texture', 'kapi1.png')))
            self.dogru_bilgiresim = ImageTk.PhotoImage(Image.open(self.get_path('texture', 'dogrubilgi.jpg')))
            self.yanlis_bilgiresim = ImageTk.PhotoImage(Image.open(self.get_path('texture', 'yanlisbilgi.png')))
            self.katiki_resim1 = ImageTk.PhotoImage(Image.open(self.get_path('texture', 'agac.png')))
            
            # Animasyon için frame'leri yükleme
            boss_gif_path = self.get_path('texture', 'boss.gif')
            self.bossgif_image = [PhotoImage(file=boss_gif_path, format=f'gif -index {i}') for i in range(self.frameCnt)]
        except Exception as e:
            print("Görseller yüklenirken hata oluştu. Varsayılan görseller kullanılmayabilir.", e)
            
    def load_questions(self):
        # Eski sistemde sorular ve cevapları ayrı ayrı koda gömülmüştü. 
        # Bunu veri yapısı haline getirdik.
        self.soru_havuzu = [
            {
                "soru": "Bilgiler geçici olarak hangi bellek üzerinde tutulur?",
                "siklar": ["A) Memory Card", "B) Hard disk", "C) Rom", "D) Ram"],
                "cevap": 3 # D şıkkı (index 3)
            },
            {
                "soru": "Hangisi bilgisayar birimi değildir?",
                "siklar": ["A) Klavye", "B) Ekran", "C) Mouse", "D) Daktilo"],
                "cevap": 3
            },
            {
                "soru": "Hangisi hem girdi hem çıktı birimidir?",
                "siklar": ["A) Flash Bellek", "B) ROM Bellek", "C) Ekran Kartı", "D) Ekran"],
                "cevap": 0
            },
            {
                "soru": "Hangisi bilgisayarın hızını etkilemez?",
                "siklar": ["A) İşlemci", "B) Yüklü programlar", "C) Mouse", "D) Ram"],
                "cevap": 2
            },
            {
                "soru": "Hangisi bir çıktı ünitesidir?",
                "siklar": ["A) Klavye", "B) Mouse", "C) Barkod Okuyucu", "D) Hoparlör"],
                "cevap": 3
            },
            {
                "soru": "Bilgisayar bellek birimlerinden 1 byte, kaç bit’ten oluşur?",
                "siklar": ["A) 3", "B) 6", "C) 8", "D) 10"],
                "cevap": 2
            },
            {
                "soru": "Bilgilerin kalıcı olarak depolandığı yere ne ad verilir?",
                "siklar": ["A) Ram", "B) Modem", "C) HDD", "D) Rom"],
                "cevap": 2
            },
            {
                "soru": "Bilgisayarı insanlardan ayıran en önemli özellik nedir?",
                "siklar": ["A) İşlem hacmi", "B) Yorum yeteneği", "C) Düşünme gücü", "D) Mantık yürütme"],
                "cevap": 0
            },
            {
                "soru": "Klavyedeki ($ , # , vb.) simgeler hangi yardımcı tuşla eklenebilir?",
                "siklar": ["A) Alt Gr", "B) Ctrl+Alt", "C) Ctrl", "D) Shift"],
                "cevap": 1
            },
            {
                "soru": "Ekrandaki en küçük noktalara ne ad verilir?",
                "siklar": ["A) Character", "B) Column", "C) Pixel", "D) Line"],
                "cevap": 2
            }
        ]
        
    def setup_launcher(self):
        # Arka plan resmi
        if hasattr(self, 'launcher_image1'):
            self.bg_label = Label(self.root, image=self.launcher_image1, justify=CENTER)
            self.bg_label.pack()
            
        self.launcher_label = Label(self.root, text="Hoş geldin savaşçı", font=("Arial", 12, "bold"))
        self.launcher_label.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.isim_girin_label = Label(self.root, text="İsim Giriniz", fg="white", bg="black", font=("Arial", 10))
        self.isim_girin_label.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.isim_giris = Entry(self.root)
        self.isim_giris.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.giris_button = Button(self.root, text="Başla", bg="black", fg="white", command=self.basla_sorgu)
        self.giris_button.place(relx=0.5, rely=0.8, anchor=CENTER)

        self.kapi_button = Button(self.root, text="Kapı Bilgisi", bg="black", fg="white", command=self.kapilar_bilgi)
        self.kapi_button.place(relx=0.2, rely=0.8, anchor=CENTER)

    def basla_sorgu(self):
        isim = self.isim_giris.get().strip()
        if not isim:
            messagebox.showinfo("Boş", "Lütfen bir isim girin!")
        else:
            self.oyuncu_ismi = isim
            self.root.withdraw() # Launcher'ı gizle
            self.baslat_hikaye()
            
    def kapilar_bilgi(self):
        try:
            with open(self.get_path("Metin", "Kapilar"), "r", encoding="utf-8") as f:
                bilgi = f.read()
            messagebox.showinfo(title="Kapılar Hakkında Bilgiler", message=bilgi)
        except Exception as e:
            messagebox.showerror("Hata", f"Kapılar dosyası bulunamadı: {e}")

    def baslat_hikaye(self):
        self.hikaye_sayac = 0
        self.story_window = Toplevel(self.root)
        self.story_window.title("Hikaye")
        self.story_window.resizable(width=False, height=False)
        self.story_window.geometry("800x400")

        if hasattr(self, 'story_resim1'):
            Label(self.story_window, image=self.story_resim1, bg="black").pack()

        self.story_label = Label(self.story_window, fg="white", bg="black", width=85, height=15, font=("Arial", 10))
        self.story_label.place(relx=0.5, rely=0.2, anchor=CENTER)
        
        self.story_button = Button(self.story_window, text="Oku", bg="black", fg="white", width=12, command=self.hikaye_ilerlet)
        self.story_button.place(x=600, y=300)
        
        # İlk hikaye satırını yükle
        try:
            with open(self.get_path("Metin", "Hikaye"), "r", encoding="utf-8") as f:
                self.hikaye_satirlari = [line.strip() for line in f.readlines() if line.strip()]
        except Exception as e:
            self.hikaye_satirlari = ["Hikaye dosyası bulunamadı..."]
            
        self.hikaye_ilerlet()

    def hikaye_ilerlet(self):
        if self.hikaye_sayac < len(self.hikaye_satirlari):
            self.story_label.config(text=self.hikaye_satirlari[self.hikaye_sayac])
            self.hikaye_sayac += 1
            if self.hikaye_sayac == len(self.hikaye_satirlari):
                self.story_button.config(text="Oyuna Başla", command=self.baslat_boss_konusma)
        else:
            self.baslat_boss_konusma()

    def baslat_boss_konusma(self):
        self.story_window.destroy()
        self.konusma_sayac = 0
        
        self.boss_window = Toplevel(self.root)
        self.boss_window.title("Konuşma")
        self.boss_window.resizable(width=False, height=False)
        self.boss_window.geometry("800x400")

        self.konusma_gif_label = Label(self.boss_window, bg="black")
        self.konusma_gif_label.pack()
        
        # Animasyon başlat
        if hasattr(self, 'bossgif_image'):
            self.boss_anim_index = 0
            self.update_boss_anim()

        self.konusma_label = Label(self.boss_window, text="Sen kimsin?", fg="white", bg="black", width=65, height=5, font=("Arial", 10))
        self.konusma_label.place(relx=0.5, rely=0.8, anchor=CENTER)   

        self.boss_button = Button(self.boss_window, text="Konuş", bg="black", fg="white", width=12, command=self.konusma_ilerlet)
        self.boss_button.place(relx=0.9, rely=0.9, anchor=CENTER)   

    def update_boss_anim(self):
        if not self.boss_window.winfo_exists(): return
        frame = self.bossgif_image[self.boss_anim_index]
        self.boss_anim_index = (self.boss_anim_index + 1) % self.frameCnt
        self.konusma_gif_label.configure(image=frame)
        self.boss_window.after(100, self.update_boss_anim)

    def konusma_ilerlet(self):
        self.konusma_sayac += 1
        diyaloglar = [
            "Seni tanımıyorum.",
            f"Demek adın {self.oyuncu_ismi}",
            "Sen bana uygun bir rakip değilsin.",
            "Şimdi yıkıl karşımdan!"
        ]
        
        if self.konusma_sayac <= len(diyaloglar):
            self.konusma_label.config(text=diyaloglar[self.konusma_sayac - 1])
            if self.konusma_sayac == len(diyaloglar):
                self.boss_button.config(text="Kabul Et (1. Kat)", command=self.baslat_kat_bir)

    def baslat_kat_bir(self):
        if hasattr(self, 'boss_window') and self.boss_window.winfo_exists():
            self.boss_window.destroy()
            
        self.kat_bir_window = Toplevel(self.root)
        self.kat_bir_window.title("Birinci Kat")
        self.kat_bir_window.geometry("800x600")
        self.kat_bir_window.resizable(width=False, height=False)

        if hasattr(self, 'katbir_resim1'):
            Label(self.kat_bir_window, image=self.katbir_resim1, bg="black").pack()

        Label(self.kat_bir_window, text=f"Hoş geldin savaşçı {self.oyuncu_ismi}", bg="black", fg="white", font=("Arial", 14, "bold")).place(relx=0.5, rely=0.1, anchor=CENTER)

        kapi_img = self.katbir_kapiresim1 if hasattr(self, 'katbir_kapiresim1') else None
        
        btn_kapi1 = Button(self.kat_bir_window, text="Kapı 1", bg="black", fg="white", image=kapi_img, compound=TOP, command=self.soru_goster)
        btn_kapi1.place(relx=0.2, rely=0.5, anchor=CENTER)

        btn_kapi2 = Button(self.kat_bir_window, text="Kapı 2", bg="black", fg="white", image=kapi_img, compound=TOP, command=self.soru_goster)
        btn_kapi2.place(relx=0.8, rely=0.5, anchor=CENTER)

    def soru_goster(self):
        self.kat_bir_window.destroy()
        self.oyun_sayac += 1
        
        self.soru_window = Toplevel(self.root)
        self.soru_window.title(f"Soru {self.oyun_sayac}")
        self.soru_window.geometry("800x600")
        self.soru_window.resizable(width=False, height=False)

        if hasattr(self, 'katbir_resim1'):
            Label(self.soru_window, image=self.katbir_resim1, bg="black").pack()

        if self.oyun_sayac <= self.oyun_sayisi:
            # Rastgele bir soru çek
            self.secilen_soru = random.choice(self.soru_havuzu)
            
            Label(self.soru_window, text=self.secilen_soru["soru"], bg="black", fg="white", font=("Arial", 14)).place(relx=0.5, rely=0.2, anchor=CENTER)
            
            # Şıkları yerleştir
            x_pos = 150
            for i, sik in enumerate(self.secilen_soru["siklar"]):
                Button(self.soru_window, text=sik, bg="gray", fg="white", width=15, height=2, 
                       command=lambda idx=i: self.cevap_kontrol(idx)).place(x=x_pos, y=400)
                x_pos += 150
        else:
            Label(self.soru_window, text=f"Bitti sanıyorsan yanılıyorsun,\n{self.oyuncu_ismi}!", bg="black", fg="white", font=("Arial", 16, "bold")).place(relx=0.5, rely=0.3, anchor=CENTER)
            Button(self.soru_window, text="Diğer Kata Geç", bg="darkred", fg="white", font=("Arial", 12), command=self.baslat_kat_iki).place(relx=0.5, rely=0.8, anchor=CENTER)

    def cevap_kontrol(self, secilen_index):
        # Ses çalma örneği
        try:
            pygame.mixer.music.load(self.get_path("music", "basari.mp3"))
            pygame.mixer.music.play()
        except Exception:
            pass

        self.soru_window.destroy()
        
        is_correct = (secilen_index == self.secilen_soru["cevap"])
        
        self.sonuc_window = Toplevel(self.root)
        self.sonuc_window.geometry("400x250")
        self.sonuc_window.resizable(width=False, height=False)
        
        if is_correct:
            self.dogru_sayac += 1
            self.sonuc_window.title("Doğru Bildin")
            img = self.dogru_bilgiresim if hasattr(self, 'dogru_bilgiresim') else None
            mesajlar = [
                f"Bu kolaydı\n{self.oyuncu_ismi}",
                "Nasıl bildin bunu seni sefil?",
                f"Tahmin ettiğimden iyi bir savaşçısın\n{self.oyuncu_ismi}"
            ]
            mssg = mesajlar[min(self.dogru_sayac - 1, len(mesajlar) - 1)]
        else:
            self.health -= 1
            self.sonuc_window.title("Yanlış Bildin")
            img = self.yanlis_bilgiresim if hasattr(self, 'yanlis_bilgiresim') else None
            mssg = f"Yanlış! Canın azaldı. Kalan Can: {self.health}"

        if img:
            Label(self.sonuc_window, image=img).pack()
            
        Label(self.sonuc_window, text=mssg, bg="black", fg="white", font=("Arial", 12, "bold")).place(relx=0.5, rely=0.2, anchor=CENTER)
        
        # Eğer canımız 0 olursa oyunu kaybettik senaryosu eklenebilir.
        if self.health <= 0:
            Button(self.sonuc_window, text="Kaybettin (Çıkış)", bg="darkred", fg="white", command=self.root.quit).place(relx=0.5, rely=0.8, anchor=CENTER)
        else:
            Button(self.sonuc_window, text="Devam Et", bg="black", fg="white", command=self.baslat_kat_bir_from_sonuc).place(relx=0.5, rely=0.8, anchor=CENTER)

    def baslat_kat_bir_from_sonuc(self):
        self.sonuc_window.destroy()
        self.baslat_kat_bir()

    def baslat_kat_iki(self):
        self.soru_window.destroy()
        self.kat_iki_window = Toplevel(self.root)
        self.kat_iki_window.title("İkinci Kat")
        self.kat_iki_window.geometry("800x600")
        self.kat_iki_window.resizable(width=False, height=False)

        if hasattr(self, 'katiki_resim1'):
            Label(self.kat_iki_window, image=self.katiki_resim1, bg="black").pack()

        Label(self.kat_iki_window, text="Devam Edecektir...", bg="black", fg="white", font=("Arial", 20, "bold")).place(relx=0.5, rely=0.5, anchor=CENTER)
        Button(self.kat_iki_window, text="Çıkış", bg="darkred", fg="white", font=("Arial", 12), command=self.root.quit).place(relx=0.5, rely=0.8, anchor=CENTER)


if __name__ == "__main__":
    root = Tk()
    app = GameApp(root)
    root.mainloop()
