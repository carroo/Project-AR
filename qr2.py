import cv2
from pyzxing import BarCodeReader

# Inisialisasi pembaca barcode
barcode_reader = BarCodeReader()

# Buka koneksi ke webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Tidak dapat membuka aliran video dari kamera.")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Tidak dapat membaca frame.")
            break

        # Simpan frame sementara ke file untuk diproses oleh ZXing
        cv2.imwrite('temp_frame.png', frame)
        result = barcode_reader.decode('temp_frame.png')

        if result:
            for barcode in result:
                points = barcode['points']
                n = len(points)
                for j in range(n):
                    cv2.line(frame, tuple(points[j]), tuple(points[(j + 1) % n]), (0, 255, 0), 2)
                cv2.putText(frame, barcode['raw'], (points[0][0], points[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Tampilkan frame hasil
        cv2.imshow('Webcam Feed with QR Code Detection', frame)

        # Tekan 'q' untuk keluar dari loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Ketika semuanya selesai, lepaskan capture
    cap.release()
    cv2.destroyAllWindows()
