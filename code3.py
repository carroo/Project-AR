import cv2
from pyzbar.pyzbar import decode

# Inisialisasi kamera
cap = cv2.VideoCapture(0)

while True:
    # Ambil frame dari kamera
    ret, frame = cap.read()
    
    if not ret:
        break

    # Decode QR codes dari frame
    decoded_objects = decode(frame)

    for obj in decoded_objects:
        # Ambil data QR code
        qr_data = obj.data.decode('utf-8')
        qr_type = obj.type

        # Gambar bounding box di sekitar QR code
        points = obj.polygon
        if len(points) == 4:
            pts = [(point.x, point.y) for point in points]
            cv2.polylines(frame, [np.array(pts, dtype=np.int32)], True, (0, 255, 0), 2)
        else:
            hull = cv2.convexHull(np.array([point.x, point.y] for point in points))
            cv2.polylines(frame, [hull], True, (0, 255, 0), 3)

        # Tampilkan data QR code
        cv2.putText(frame, qr_data, (obj.rect.left, obj.rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Tampilkan frame
    cv2.imshow('QR Code Scanner', frame)

    # Keluar jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Hentikan kamera dan tutup jendela
cap.release()
cv2.destroyAllWindows()
