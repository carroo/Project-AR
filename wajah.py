import cv2
import mediapipe as mp

# Inisialisasi modul MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Buka koneksi ke webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Tidak dapat membuka aliran video dari kamera.")
else:
    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Gagal menangkap gambar")
                break

            # Ubah warna frame ke RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)

            # Jika ada deteksi wajah
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Gambar landmark pada wajah
                    mp_drawing.draw_landmarks(
                        frame, face_landmarks, mp_face_mesh.FACE_CONNECTIONS,
                        mp_drawing_styles.get_default_face_mesh_tesselation_style(),
                        mp_drawing_styles.get_default_face_mesh_contours_style(),
                        mp_drawing_styles.get_default_face_mesh_iris_connections_style())

                    # Akses dan analisis landmark
                    for id, lm in enumerate(face_landmarks.landmark):
                        ih, iw, _ = frame.shape
                        x, y = int(lm.x * iw), int(lm.y * ih)
                        if id == 0:  # Landmark ID 0 adalah ujung hidung
                            cv2.putText(frame, 'Nose', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # Tampilkan frame hasil
            cv2.imshow('Webcam Feed with Face Mesh', frame)

            # Tekan 'q' untuk keluar dari loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Ketika semuanya selesai, lepaskan capture
    cap.release()
    cv2.destroyAllWindows()
