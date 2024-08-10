import cv2

# Initialize QR code detector
qr_code_detector = cv2.QRCodeDetector()

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open video stream from camera.")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read frame.")
            break

        # Detect and decode QR code
        data, bbox, _ = qr_code_detector.detectAndDecode(frame)
        if bbox is not None:
            # Ensure bbox is in the right format
            bbox = bbox.astype(int)  # Convert to integer if needed
            for i in range(len(bbox)):
                cv2.line(frame, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)

            if data:
                cv2.putText(frame, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Display frame
        cv2.imshow('Webcam Feed with QR Code Detection', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release capture when done
    cap.release()
    cv2.destroyAllWindows()
