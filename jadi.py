import cv2
import requests
import numpy as np

# Initialize QR code detector
qr_code_detector = cv2.QRCodeDetector()

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open video stream from camera.")
else:
    last_data = None  # Variable to store the last detected QR code data
    last_img = None   # Variable to store the last loaded image
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read frame.")
            break

        # Detect and decode QR code
        data, bbox, _ = qr_code_detector.detectAndDecode(frame)
        if bbox is not None:
            bbox = bbox.astype(int)
            for i in range(len(bbox)):
                cv2.line(frame, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)

            if data:
                # Only process the QR code if it's different from the last one
                if data != last_data:
                    last_data = data  # Update last_data

                    # Check if data is a URL pointing to an image
                    if data.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        try:
                            response = requests.get(data)
                            img_array = np.array(bytearray(response.content), dtype=np.uint8)
                            last_img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # Store last loaded image

                        except Exception as e:
                            print(f"Error loading image from URL: {e}")

        # Overlay the last loaded image if available and QR code is detected
        if last_img is not None and data:
            qr_width = int(bbox[0][1][0] - bbox[0][0][0])
            qr_height = int(bbox[0][2][1] - bbox[0][1][1])
            
            # Resize the last loaded image to match the size of the QR code
            img_resized = cv2.resize(last_img, (qr_width, qr_height))
            
            top_left_x = max(0, min(int(bbox[0][0][0]), frame.shape[1] - qr_width))
            top_left_y = max(0, min(int(bbox[0][0][1]), frame.shape[0] - qr_height))

            # Place the resized image in the calculated position
            frame[top_left_y:top_left_y + qr_height, top_left_x:top_left_x + qr_width] = img_resized

        # Display frame
        cv2.imshow('Webcam Feed with QR Code Detection', frame)

        # Press 'q' to exit
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

    # Release capture when done
    cap.release()
    cv2.destroyAllWindows()
