#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARP Spoofing Tespit Aracı - Spotify UI Versiyonu
Bu araç, ağda olası ARP spoofing saldırılarını tespit etmek için gerekli tüm fonksiyonları ve 
tkinter tabanlı Spotify tarzında bir grafik arayüz içerir.

Versiyon: 2.0 - Windows Uyumlu
"""

import os
import sys
import tkinter as tk
import ctypes  # Admin yetkilerini kontrol etmek için
from tkinter import messagebox  # Mesaj kutuları için

# Debug için print'ler ekleyelim
print("Program başlatılıyor...")

# Pystray için gerekli modüller
try:
    import PIL.Image
    import pystray
    HAS_PYSTRAY = True
    print("Pystray başarıyla import edildi.")
except ImportError:
    HAS_PYSTRAY = False
    print("Uyarı: pystray veya PIL modülü bulunamadı. Sistem tepsisi özellikleri devre dışı.")

# Gerekli modüller
import socket
import re
import threading
import time
import subprocess
import logging  # Hata ayıklama için
from collections import defaultdict

# ui modüllerini import etmeye çalışalım
print("UI modülleri import ediliyor...")
try:
    from ui.screens import SpotifyARPApp
    print("SpotifyARPApp başarıyla import edildi.")
except Exception as e:
    print(f"SpotifyARPApp import edilirken hata: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)  # Hatayla çık

# Debug modunu etkinleştir
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Global değişkenler
root = None
app = None
icon = None

def start_desktop_app():
    """Desktop uygulamasını başlatır"""
    try:
        print("Tkinter UI başlatılıyor...")
        
        global root, app, icon
        
        # Ana tkinter penceresini oluştur
        root = tk.Tk()
        print("Tkinter penceresi oluşturuldu.")
        
        root.title("ARP Spoofing Tespit Aracı")
        root.geometry("1000x650")
        root.minsize(800, 600)
        print("Pencere boyutları ayarlandı.")
        
        # Ana uygulama sınıfını oluştur
        print("SpotifyARPApp oluşturuluyor...")
        app = SpotifyARPApp(root)
        print("SpotifyARPApp başarıyla oluşturuldu.")
        
        # Kapatma işlemi yeniden tanımla
        def on_close():
            print("Kapatma isteği alındı.")
            # Periyodik tarama aktif mi kontrol et
            periodic_active = False
            if hasattr(app, 'scanner'):
                periodic_active = getattr(app.scanner, 'periodic_running', False)
                print(f"Periyodik tarama aktif: {periodic_active}")
            
            if periodic_active:
                # Periyodik tarama aktifse
                if messagebox.askyesno("Kapat", "Periyodik tarama aktif. Uygulama kapatılsa bile arka planda çalışmaya devam edecektir.\n\nDevam etmek istiyor musunuz?"):
                    if HAS_PYSTRAY:
                        print("Pencere gizleniyor ve sistem tepsisine alınıyor.")
                        root.withdraw()  # Pencereyi gizle
                        create_system_tray()  # Sistem tepsisi oluştur
                    else:
                        # Pystray yoksa, kullanıcıya bilgi ver
                        print("Pystray yok, uygulama tamamen kapatılıyor.")
                        messagebox.showinfo("Bilgi", "Sistem tepsisi desteği olmadığı için uygulama tamamen kapatılacak.")
                        root.destroy()
            else:
                # Periyodik tarama aktif değilse normal kapat
                if messagebox.askyesno("Kapat", "Uygulamayı kapatmak istiyor musunuz?"):
                    print("Uygulama kapatılıyor.")
                    root.destroy()
        
        # Pencere kapatma olayını yakala
        root.protocol("WM_DELETE_WINDOW", on_close)
        
        print("Uygulama başarıyla başlatıldı! Mainloop'a giriliyor...")
        
        # Uygulamayı başlat
        root.mainloop()
        print("Mainloop'dan çıkıldı.")
    except Exception as e:
        print(f"Uygulama başlatılırken hata oluştu: {e}")
        import traceback
        traceback.print_exc()

def create_system_tray():
    """Sistem tepsisi ikonu oluşturur"""
    print("Sistem tepsisi oluşturuluyor...")
    if not HAS_PYSTRAY:
        print("Pystray yok, sistem tepsisi oluşturulamıyor.")
        return
        
    global icon, root, app
    
    # Logo için PIL görüntüsü oluştur
    try:
        image_path = os.path.join(os.path.dirname(__file__), "assets", "shield.png")
        if os.path.exists(image_path):
            print(f"Logo bulundu: {image_path}")
            image = PIL.Image.open(image_path)
        else:
            print("Logo bulunamadı, basit bir görüntü oluşturuluyor.")
            # Basit bir siyah kare oluştur
            image = PIL.Image.new('RGB', (16, 16), color = (0, 0, 0))
    except Exception as e:
        print(f"Logo yüklenirken hata: {e}")
        # Hata durumunda basit bir görüntü oluştur
        image = PIL.Image.new('RGB', (16, 16), color = (0, 0, 0))
    
    # Menü işlevleri
    def show_window(icon, item):
        print("Pencereyi göster komutu alındı.")
        icon.stop()  # İkonu durdur
        root.after(0, root.deiconify)  # Ana pencereyi göster
    
    def exit_app(icon, item):
        print("Tamamen kapat komutu alındı.")
        # Periyodik taramayı durdur
        if hasattr(app, 'scanner'):
            app.scanner.stop_periodic_scan()
        icon.stop()  # İkonu durdur
        root.after(0, root.destroy)  # Uygulamayı tamamen kapat
    
    # Menü oluştur
    print("Sistem tepsisi menüsü oluşturuluyor...")
    menu = pystray.Menu(
        pystray.MenuItem("ARP Tarama Aracını Göster", show_window),
        pystray.MenuItem("Tamamen Kapat", exit_app)
    )
    
    # İkonu oluştur ve başlat
    print("Sistem tepsisi ikonu oluşturuluyor...")
    icon = pystray.Icon("arp_shield", image, "ARP Tarama Aracı (Arka planda çalışıyor)", menu)
    
    # İkonu ayrı bir thread'de başlat
    print("Sistem tepsisi ikonu thread'de başlatılıyor...")
    threading.Thread(target=icon.run, daemon=True).start()

if __name__ == "__main__":
    print("Ana program başlatılıyor...")
    # Masaüstü uygulamasını doğrudan başlat
    start_desktop_app()
    print("Program sonlandı.")