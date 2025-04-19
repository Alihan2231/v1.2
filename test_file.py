# test_file.py adlı dosya

try:
    with open("test_write.txt", "w") as f:
        f.write("Bu bir test yazısıdır")
    print("Dosya başarıyla yazıldı!")
    
    with open("test_write.txt", "r") as f:
        content = f.read()
    print(f"Dosya içeriği: {content}")
except Exception as e:
    print(f"Hata: {e}")

input("Devam etmek için Enter tuşuna basın...")
