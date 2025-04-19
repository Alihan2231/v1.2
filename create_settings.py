#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

# Ayarlar dosyasının yolu
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

# Varsayılan ayarlar
DEFAULT_SETTINGS = {
    "scan_interval": 24,  # Periyodik tarama aralığı (saat)
    "auto_start_periodic": False,  # Uygulama başladığında periyodik taramayı otomatik başlat
    "notifications_enabled": True,  # Bildirimler etkin mi
    "dark_mode": True,  # Koyu tema etkin mi
    "last_scan_timestamp": None,  # Son tarama zamanı
    "periodic_scan_active": False,  # Periyodik tarama şu anda aktif mi
    "custom_settings": {}  # Diğer özel ayarlar
}

print(f"Ayarlar dosyası oluşturuluyor: {SETTINGS_FILE}")

try:
    # Ayarları dosyaya kaydet
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(DEFAULT_SETTINGS, f, indent=4, ensure_ascii=False)
    print(f"Ayarlar dosyası başarıyla oluşturuldu: {SETTINGS_FILE}")
    
    # Dosya izinlerini göster
    import stat
    file_stat = os.stat(SETTINGS_FILE)
    file_mode = stat.filemode(file_stat.st_mode)
    print(f"Dosya izinleri: {file_mode}")
    
    # Dosya içeriğini göster
    with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
        settings = json.load(f)
    print("\nAyarlar dosyası içeriği:")
    print(json.dumps(settings, indent=4, ensure_ascii=False))
    
except Exception as e:
    import traceback
    print(f"Hata oluştu: {e}")
    traceback.print_exc()

input("\nDevam etmek için Enter tuşuna basın...")
