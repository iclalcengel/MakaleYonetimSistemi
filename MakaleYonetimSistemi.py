#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlite3

veri = sqlite3.connect("MakaleYonetimSistemi.db") #MakaleYonetimSistemi.db adli database dosyasini olusturur ve bizi ona baglar.
cursor = veri.cursor() # Database uzerindeki islemler bu cursor uzerinden yapiliyor.


def tablolar_olustur():
     # Kullanıcılar tablosu
    cursor.execute("CREATE TABLE IF NOT EXISTS Kullanicilar (KullaniciId INTEGER PRIMARY KEY, KullaniciAdi TEXT, Sifre TEXT, Eposta TEXT, RolId INTEGER, FOREIGN KEY (RolId) REFERENCES Roller(RolId))")

    # Roller tablosu
    cursor.execute("CREATE TABLE IF NOT EXISTS Roller (RolId INTEGER PRIMARY KEY, RolAdi TEXT)")

    # Makaleler tablosu
    cursor.execute("CREATE TABLE IF NOT EXISTS Makaleler (MakaleId INTEGER PRIMARY KEY, Baslik TEXT, Yazarlar TEXT, YazarEposta TEXT, YazarKurum TEXT, YuklemeTarihi DATE, Durum TEXT)")

    # Hakem Atamaları tablosu
    cursor.execute("CREATE TABLE IF NOT EXISTS HakemAtamalari (MakaleId INTEGER, HakemId INTEGER, AtamaTarihi DATE, DegerlendirmeDurumu TEXT, FOREIGN KEY (MakaleId) REFERENCES Makaleler(MakaleId), FOREIGN KEY (HakemId) REFERENCES Kullanicilar(KullaniciId))")

    veri.commit()
    # Her islemden sonra database uzerinde bu verilerin guncellenmesi icin commit metodunu kullanmamiz gerekir.

#Olusturdugumuz bu fonksiyonu cagiriyoruz.
tablolar_olustur()   
 
def rol_ekle():
    # Roller tablosuna veri ekle
    cursor.execute("INSERT INTO Roller (RolId, RolAdi) VALUES (1, 'Yazar'), (2, 'Editör'), (3, 'Hakem')")

def kullanici_ekle():
    # Kullanıcılar tablosuna veri ekle
    cursor.execute("INSERT INTO Kullanicilar (KullaniciAdi, Sifre, Eposta, RolId) VALUES ('yazar', 'parola1', 'eposta1@ornek.com', 1), ('editor', 'parola2', 'eposta2@ornek.com', 2), ('hakem', 'parola3', 'eposta3@ornek.com', 3)")

def makale_ekle(baslik, yazarlar, yazar_eposta, yazar_kurum, yukleme_tarihi, durum):
    cursor.execute("INSERT INTO Makaleler (Baslik, Yazarlar, YazarEposta, YazarKurum, YuklemeTarihi, Durum) VALUES (?, ?, ?, ?, ?, ?)", (baslik, yazarlar, yazar_eposta, yazar_kurum, yukleme_tarihi, durum))
    veri.commit()
    
def hakem_atamaları_ekle():
    # Hakem Atamalari tablosuna veri ekle
    cursor.execute("INSERT INTO HakemAtamalari (MakaleId, HakemId, AtamaTarihi, DegerlendirmeDurumu) VALUES (?, ?, ?, ?)", (1, 3, '2023-01-03', 'kabul'))
    cursor.execute("INSERT INTO HakemAtamalari (MakaleId, HakemId, AtamaTarihi, DegerlendirmeDurumu) VALUES (?, ?, ?, ?)", (2, 3, '2023-01-20', 'ret'))
    veri.commit()

def yazar_verilerini_al():
    # Database üzerindeki verilerin çağrılması yapılıyor.
    cursor.execute('SELECT MakaleId, Baslik, Yazarlar, YuklemeTarihi, Durum FROM Makaleler')
    liste = cursor.fetchall()
    print('Makale bilgileri yükleniyor...')
    for makale in liste:
        
        makale_id, baslik, yazarlar, yukleme_tarihi, durum = makale
        print(f"Makale ID: {makale_id}, Başlık: {baslik}, Yazarlar: {yazarlar}, Yükleme Tarihi: {yukleme_tarihi}, Durum: yüklendi")
        
def editor_verilerini_al():
    # Database üzerindeki verilerin çağrılması yapılıyor.
    cursor.execute('SELECT MakaleId, HakemId, AtamaTarihi, DegerlendirmeDurumu FROM HakemAtamalari')
    liste = cursor.fetchall()
    print('Atama bilgileri yükleniyor...')
    for hakematamasi in liste:
        
        MakaleId, HakemId, AtamaTarihi, DegerlendirmeDurumu = hakematamasi
        print(f"Makale ID: {MakaleId}, Hakem ID: {HakemId}, Atama Tarihi: {AtamaTarihi}, Durum: {DegerlendirmeDurumu}")

    
def yazar_yukleme_tarihleri_goruntule():               #yükleme tarihi verisini çekmek için fonksiyon 
    cursor.execute('SELECT YuklemeTarihi FROM Makaleler')
    yukleme_tarihleri = cursor.fetchall()
    print('Makale Yükleme Tarihleri:')
    for tarih in yukleme_tarihleri:
        print(tarih[0])

        
def hakem_verilerini_al():
    # Database uzerindeki verilerin cagirilmasi yapiliyor.
    cursor.execute('SELECT * FROM HakemAtamalari')
    liste = cursor.fetchall()
    print('Hakem bilgileri yukleniyor...')
    for i in liste:
        print(i)

def durum_degis(eski,yeni):
    # Bu fonksiyonlar sayesinde sinif,okul,sube degisiklikleri yapiliyor.
    cursor.execute("UPDATE Makaleler set Durum = ? where Durum = ?",(yeni,eski))
    veri.commit()
    
def giris_yap():
    
    kullanici_adi = input("Kullanıcı Adı: ")
    sifre = input("Şifre: ")

    # Kullanıcı adı sözlükte var mı ve şifre doğru mu kontrol et
    if kullanici_adi in kullanicilar and kullanicilar[kullanici_adi] == sifre:
        print("Giriş başarılı!")
        return kullanici_adi
    else:
        print("Kullanıcı adı veya şifre yanlış!")
        return None
    
def degerlendirmedurumu_degis(eski,yeni):
    cursor.execute("UPDATE HakemAtamaları set DegerlendirmeDurumu = ? where DegerlendirmeDurumu = ?",(yeni,eski))
    veri.commit()
    
def kullanici_kayit():
    kullanici_adi = input("Kullanıcı Adı: ")
    sifre = input("Şifre: ")
    eposta = input("E-posta: ")
    rol_id = input("Rol ID: ")

    # Kullanıcıyı veritabanına ekle
    cursor.execute("INSERT INTO Kullanicilar (KullaniciAdi, Sifre, Eposta, RolId) VALUES (?, ?, ?, ?)",
                   (kullanici_adi, sifre, eposta, rol_id))
    veri.commit()
    rol_ekle()
    print("Kullanıcı başarıyla kaydedildi!")
    
def yazar_makale_ekle(baslik, yazarlar, yazar_eposta, yazar_kurum, yukleme_tarihi, durum):
    cursor.execute("INSERT INTO Makaleler (Baslik, Yazarlar, YazarEposta, YazarKurum, YuklemeTarihi, Durum) VALUES (?, ?, ?, ?, ?, ?)", (baslik, yazarlar, yazar_eposta, yazar_kurum, yukleme_tarihi, durum))
    veri.commit()

    # Yüklenen makalenin durumunu güncelle
    cursor.execute("UPDATE Makaleler SET Durum = 'yüklendi' WHERE Baslik = ? AND YuklemeTarihi = ?", (baslik, yukleme_tarihi))
    veri.commit()
    
    hakem_atamaları_ekle()
    
def makale_sec_ve_hakem_atama():
    cursor.execute("SELECT MakaleId, Baslik, Durum FROM Makaleler WHERE Durum = 'yüklendi'")
    makaleler = cursor.fetchall()

    print("Atama yapılacak makaleler:")
    for makale in makaleler:
        print(f"Makale ID: {makale[0]}, Başlık: {makale[1]}")

    makale_id = input("Atama yapmak istediğiniz makalenin ID'sini girin: ")

    cursor.execute("SELECT KullaniciId, KullaniciAdi FROM Kullanicilar WHERE RolId = 3")  # Hakemleri getir
    hakemler = cursor.fetchall()

    print("Atanabilecek hakemler:")
    for hakem in hakemler:
        print(f"Hakem ID: {hakem[0]}, Kullanıcı Adı: {hakem[1]}")

    HakemId = input("Atamak istediğiniz hakemin ID'sini girin: ")

    # Seçilen makale ve hakemi atama
    cursor.execute("INSERT INTO HakemAtamalari (MakaleId, HakemId, AtamaTarihi, DegerlendirmeDurumu) VALUES (?, ?, DATE('now'), 'Degerlendirmede')", (makale_id, HakemId))
    veri.commit()
    print("Hakem ataması başarıyla yapıldı.")
    
    hakem_atamaları_ekle()
    
def degerlendirmede_makaleleri_goruntule():
    cursor.execute("SELECT Makaleler.MakaleId, Makaleler.Baslik, HakemAtamalari.HakemId, HakemAtamalari.AtamaTarihi, COALESCE(HakemAtamalari.DegerlendirmeDurumu, 'Yüklendi') FROM Makaleler LEFT JOIN HakemAtamalari ON Makaleler.MakaleId = HakemAtamalari.MakaleId WHERE COALESCE(HakemAtamalari.DegerlendirmeDurumu, 'Yüklendi') = 'Degerlendirmede'")
    makaleler = cursor.fetchall()

    if len(makaleler) == 0:
        print("Değerlendirmede olan makale bulunmamaktadır.")
    else:
        print("Değerlendirmede olan makaleler:")
        for makale in makaleler:
            makale_id, baslik, HakemId, atama_tarihi, degerlendirme_durumu = makale
            if HakemId is None:
                print(f"Makale ID: {makale_id}, Başlık: {baslik}, Atanmış Hakem: Yok, Atama Tarihi: Yok, Durum: {degerlendirme_durumu}")
            else:
                print(f"Makale ID: {makale_id}, Başlık: {baslik}, Atanmış Hakem ID: {HakemId}, Atama Tarihi: {atama_tarihi}, Durum: {degerlendirme_durumu}")


def hakem_atanan_makaleleri_goruntule(HakemId):
    cursor.execute("SELECT Makaleler.MakaleId, Makaleler.Baslik FROM Makaleler INNER JOIN HakemAtamalari ON Makaleler.MakaleId = HakemAtamalari.MakaleId WHERE HakemAtamalari.HakemId = ?", (HakemId,))
    makaleler = cursor.fetchall()

    if len(makaleler) == 0:
        print("Size atanmış makale bulunmamaktadır.")
    else:
        print("Size atanmış makaleler:")
        for makale in makaleler:
            print(f"Makale ID: {makale[0]}, Başlık: {makale[1]}")

def makaleyi_degerlendir(makale_id, HakemId, karar):
    if karar.lower() == 'kabul' or karar.lower() == 'ret':
        cursor.execute("UPDATE HakemAtamalari SET DegerlendirmeDurumu = ? WHERE MakaleId = ? AND HakemId = ?", (karar.capitalize(), makale_id, HakemId))
        veri.commit()
        print("Makale değerlendirme durumu başarıyla güncellendi.")
    else:
        print("Geçersiz değerlendirme seçeneği. Lütfen 'kabul' ya da 'ret' olarak girin.")
        
def hakem_id_al(kullanici_adi):
    cursor.execute("SELECT KullaniciId FROM Kullanicilar WHERE KullaniciAdi = ?", (kullanici_adi,))
    row = cursor.fetchone()
    if row:
        return row[0]  # Kullanıcıya ait Hakem ID'sini döndürür
    else:
        return None


print("""-----------------------------------
KOSTÜ MAKALE YÖNETİM SİSTEMİNE HOŞGELDİNİZ
İşlemler;      
[1] Giriş Yap
[2] Üye Ol
-----------------------------------""")

kullanicilar = {
    "yazar": "parola1",
    "editor": "parola2",
    "hakem": "parola3",
    "yazar2":"yazar2"
}
secenek = input("Seçenek: ")

if secenek == '1':
# Kullanıcı girişini iste ve kullanıcı adını al
 kullanici_tipi = giris_yap()


if secenek == '2':
 kullanici_kayit()
 kullanici_tipi = giris_yap()
 
# Eğer kullanıcı adı doğruysa, ilgili menüye geç
if kullanici_tipi:
    HakemId = hakem_id_al(kullanici_tipi)
    while True:
        if kullanici_tipi == 'yazar':
            print("""-----------------------------------
            YAZAR MENÜSÜNE HOŞGELDİNİZ
            İşlemler;
            [1] Makaleleri Görüntüle
            [2] Yeni Makale Ekle
            [3] Makale Yükleme Tarihlerini Görüntüle      
            -----------------------------------""")
            islem = input("İslem seçin (1, 2 veya 3): ")

            if islem == '1':
                yazar_verilerini_al()
            elif islem == '2':
                # Yeni makale ekleme işlemi
                Baslik = input("Makale Başlığı:")
                Yazarlar = input("Yazar Ad-Soyadi:")
                YazarEposta = input('Yazar E-posta:')
                YazarKurum = input('Yazarın Çalıştığı Kurum:')
                YuklemeTarihi = input('Makalenin Yüklenme Tarihi:')
                Durum = input('Makalenin Durumu:')
                yazar_makale_ekle(Baslik, Yazarlar, YazarEposta, YazarKurum, YuklemeTarihi, Durum)
            
            elif islem == '3':
                yazar_yukleme_tarihleri_goruntule()
                
        elif kullanici_tipi == 'editor':
            print("""-----------------------------------
            EDİTÖR MENÜSÜNE HOŞGELDİNİZ
            İşlemler;
            [1] Mevcut Makale Durumlarını Görüntüle
            [2] Hakem Ataması Yapma
            -----------------------------------""")
            islem = input("İslem seçin (1 veya 2): ")

            if islem == '1':                   #mevcut makale durumları
                degerlendirmede_makaleleri_goruntule()
                
            elif islem == '2':                      #hakem ataması yapma
                makale_sec_ve_hakem_atama()
        
        elif kullanici_tipi == 'hakem' :
            print("""-----------------------------------
            HAKEM MENÜSÜNE HOŞGELDİNİZ
            İşlemler;
            [1] Makaleleri Görüntüle
            [2] Makalenin Mevcut Durumunu Değiştirme
            -----------------------------------""")
            islem = input("İslem seçin (1 veya 2): ")

            if islem == '1':
                hakem_atanan_makaleleri_goruntule(HakemId)
            elif islem == '2':
                makale_id = input("Değerlendirmek istediğiniz makalenin ID'sini girin: ")
                karar = input("Makaleyi 'kabul' veya 'ret' olarak değerlendirin: ")
                makaleyi_degerlendir(makale_id, HakemId, karar)  # Makaleyi değerlendirme


        # Çıkış yapılana kadar devam et
        cikis = input("Çıkmak için 'q' tuşuna basın: ")
        if cikis.lower() == 'q':
            print('Başarıyla çıkış yapıldı.')
            break

        



