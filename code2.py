import cv2
import numpy as np

# Fungsi untuk mendeteksi titik-titik di sudut luar gambar dan mendapatkan kode
def read_dot_code(image, dot_size=10, spacing=5):
    h, w = image.shape[:2]
    border_size = dot_size*2 + spacing*2
    new_h, new_w = h - border_size*2, w - border_size*2
    
    # Koordinat untuk tanda di kiri atas, kanan atas, kiri bawah, dan kanan bawah
    corners = [
        (0, 0),  # Kiri atas
        (w - border_size, 0),  # Kanan atas
        (0, h - border_size),  # Kiri bawah
        (w - border_size, h - border_size)  # Kanan bawah
    ]
    
    code = ""
    
    # Mengecek setiap sudut untuk menghitung titik-titik
    for cx, cy in corners:
        count = 0
        for i in range(10):  # Maksimum 10 titik di setiap sudut
            x = cx + (i % 2) * (dot_size + spacing)
            y = cy + (i // 2) * (dot_size + spacing)
            if x < w and y < h and np.all(image[y:y+dot_size, x:x+dot_size] == [0, 0, 0]):
                count += 1
        code += str(count)
    
    return code

# Muat gambar dengan titik-titik
image_with_dots = cv2.imread('image_with_dots.jpg')

# Baca kode dari titik-titik
code = read_dot_code(image_with_dots)
print(image_with_dots)
print(f"Kode yang terdeteksi: {code}")
