#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ayarlar Modülü
Bu modül, uygulama ayarlarını kaydetmek ve yüklemek için fonksiyonlar içerir.
"""

import os
import json
import logging

# Ayarlar dosyasının yolu
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings.json")

# Varsayılan ayarlar
DEFAULT_SETTINGS = {
    "scan_interval": 24,  # Periyodik tarama aralığı (saat)
    "auto_start_periodic": False,  # Uygulama başladığında periyodik taramayı otomatik başlat
    "notifications_enabled": True,  # Bildirimler etkin mi
    "dark_mode": True,  # Koyu tema etkin mi
    "last_scan_timestamp": None,  # Son tarama zamanı
    "custom_settings": {}  # Diğer özel ayarlar
}

def load_settings():
    """
    Ayarları dosyadan yükler, dosya yoksa varsayılan ayarları kullanır.
    
    Returns:
        dict: Ayarlar sözlüğü
    """
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                
            # Eksik ayarları varsayılan değerlerle doldur
            for key, value in DEFAULT_SETTINGS.items():
                if key not in settings:
                    settings[key] = value
                    
            return settings
        else:
            # Dosya yoksa varsayılan ayarları kullan
            return DEFAULT_SETTINGS.copy()
    except Exception as e:
        logging.error(f"Ayarlar yüklenirken hata: {e}")
        # Hata durumunda varsayılan ayarları kullan
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """
    Ayarları dosyaya kaydeder.
    
    Args:
        settings (dict): Kaydedilecek ayarlar sözlüğü
        
    Returns:
        bool: İşlem başarılı ise True, aksi halde False
    """
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        logging.error(f"Ayarlar kaydedilirken hata: {e}")
        return False

def get_setting(key, default=None):
    """
    Belirli bir ayarı getirir.
    
    Args:
        key (str): Ayar anahtarı
        default: Ayar bulunamazsa döndürülecek değer
        
    Returns:
        Ayar değeri veya default değeri
    """
    settings = load_settings()
    return settings.get(key, default)

def set_setting(key, value):
    """
    Belirli bir ayarı günceller ve kaydeder.
    
    Args:
        key (str): Ayar anahtarı
        value: Ayarlanacak değer
        
    Returns:
        bool: İşlem başarılı ise True, aksi halde False
    """
    settings = load_settings()
    settings[key] = value
    return save_settings(settings)

def update_settings(settings_dict):
    """
    Birden fazla ayarı aynı anda günceller.
    
    Args:
        settings_dict (dict): Güncellenecek ayarlar sözlüğü
        
    Returns:
        bool: İşlem başarılı ise True, aksi halde False
    """
    settings = load_settings()
    settings.update(settings_dict)
    return save_settings(settings)
