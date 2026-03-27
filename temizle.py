import os

dosya_adi = "fabrika.py"

with open(dosya_adi, "rb") as f:
    veri = f.read()

# BOM'u temizle
if veri.startswith(b'\xef\xbb\xbf'):
    veri = veri[3:]
    print("✅ BOM temizlendi.")
else:
    print("ℹ️ BOM yoktu, herhangi bir değişiklik yapılmadı.")

with open(dosya_adi, "wb") as f:
    f.write(veri)

print("Dosya yeniden yazıldı.")