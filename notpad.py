import customtkinter as ctk
import os
from cryptography.fernet import Fernet

app = ctk.CTk()

# Sifreleme Anahtari Yoksa Olustur
if not os.path.exists("anahtar.key"):
    with open("anahtar.key", "wb") as anahtarDosyasi:
        anahtarDosyasi.write(Fernet.generate_key())
        
# Sifreleme Anahtarini Oku
with open("anahtar.key", "rb") as anahtarDosyasi:
    gizliAnahtar = anahtarDosyasi.read()
    
# Sifreleme Ac
fernet = Fernet(gizliAnahtar)

aktifDosya = "notlar.txt"

# Uygulama Basligi ve Boyutu
app.title("YagYz Notpad")
app.geometry("400x500")

# Girilen Sifrenin Kontrolu
def girisKontrol():
    
    girilenSifre = sifreKutu.get()
    
    if girilenSifre == "12345":
        bildirimEtiketi.configure(text="Sifre Dogru! Giris Yapiliyor...", text_color="green")
        notEkrani()
        notyukle()
        
    else:
        bildirimEtiketi.configure(text="Sifre Hatali! Tekrar Deneyiniz.", text_color="red")
        
# Giris Basarili Oldugunda Calisan Not Yazma Penceresi
def notEkrani():
    global notAlani
    global kaydetmeButon
    global aktifDosyaEtiketi
    
    # Giris Sayfasini Temizleme
    baslik.destroy()
    sifreKutu.destroy()
    bildirimEtiketi.destroy()
    girisButonu.destroy() 
    
    # Ust Menu
    dosyaSekme = ctk.CTkFrame(master=app, fg_color="transparent")
    dosyaSekme.pack(pady=5, fill="x", padx=20)
    
    yeniDosyaButonu = ctk.CTkButton(master=dosyaSekme, text="+ Yeni Dosya", width=100, command=yeniDosyaOlustur)
    yeniDosyaButonu.pack(side="left", padx=5)
    
    aktifDosyaEtiketi = ctk.CTkLabel(master=dosyaSekme, text=f"Şu anki dosya: {aktifDosya}")
    aktifDosyaEtiketi.pack(side="right", padx=5)
    
    # Not Yazma Alani
    notAlani = ctk.CTkTextbox(master=app, width=350, height=300)
    notAlani.pack(pady=20)
    
    # Not Kaydetme Alani
    kaydetmeButon = ctk.CTkButton(master=app, text="Notlari Kaydet", command=notKaydet)
    kaydetmeButon.pack(pady=10)
    
def yeniDosyaOlustur():
    global aktifDosya
    
    dialog = ctk.CTkInputDialog(text="Yeni dosya adını girin (Örn: gunluk2):", title="Yeni Dosya")
    yeniIsim = dialog.get_input()
    
    if yeniIsim:
        if not yeniIsim.endswith(".txt"):
            yeniIsim += ".txt"
        
        aktifDosya = yeniIsim
        aktifDosyaEtiketi.configure(text=f"Şu anki dosya: {aktifDosya}")
        
        notAlani.delete("0.0", "end")
        notKaydet()

# Notlari Dosyaya Yazdirma Fonksiyonu
def notKaydet():
    yazilanNotlar = notAlani.get("0.0", "end")
    
    byteNotlar = yazilanNotlar.encode("utf-8")
    sifreliNotlar= fernet.encrypt(byteNotlar)
    
    with open(aktifDosya, "wb") as dosya:
        dosya.write(sifreliNotlar)
    
    kaydetmeButon.configure(text="Basariyla Kaydedildi!", text_color="green")
    app.after(2000, lambda: kaydetmeButon.configure(text="Notlari Kaydet", text_color="white"))
        
# Eski Notlari Yukleme
def notyukle():
    try:
        with open(aktifDosya, "rb") as dosya:
            sifreliOkunan = dosya.read()
            
        cozulmusByte = fernet.decrypt(sifreliOkunan)
        eskiNotlar = cozulmusByte.decode("utf-8")
        notAlani.insert("0.0", eskiNotlar)
    
    except FileNotFoundError:
        pass

# Giris Sayfasi
baslik = ctk.CTkLabel(master=app, text="YagYz Notpad`e Hosgeldiniz", font=("Helvetica", 24, "bold"))
baslik.pack(pady=40)

sifreKutu = ctk.CTkEntry(master=app, placeholder_text="Sifre Giriniz...", show="*", width=200)
sifreKutu.pack(pady=20)

bildirimEtiketi = ctk.CTkLabel(master=app, text="", font=("Helvetica", 12))
bildirimEtiketi.pack(pady=10)

girisButonu = ctk.CTkButton(master=app, text="Giris Yap", command=girisKontrol)
girisButonu.pack(pady=20)

# Ana Dongu - En altta kalmali
app.mainloop()