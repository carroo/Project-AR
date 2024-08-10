from flask import Flask, render_template, Response
import cv2
import requests
import numpy as np

app = Flask(__name__)

# Initialize QR code detector
qr_code_detector = cv2.QRCodeDetector()

# Open webcam
cap = cv2.VideoCapture(0)

def generate_frames():
    last_data = None
    last_img = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        data, bbox, _ = qr_code_detector.detectAndDecode(frame)
        if bbox is not None:
            bbox = bbox.astype(int)
            for i in range(len(bbox)):
                cv2.line(frame, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)

            if data and data != last_data:
                last_data = data
                if data.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    try:
                        response = requests.get(data)
                        img_array = np.array(bytearray(response.content), dtype=np.uint8)
                        last_img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                    except Exception as e:
                        print(f"Error loading image from URL: {e}")

        if last_img is not None and data:
            qr_width = int(bbox[0][1][0] - bbox[0][0][0])
            qr_height = int(bbox[0][2][1] - bbox[0][1][1])
            img_resized = cv2.resize(last_img, (qr_width, qr_height))

            top_left_x = max(0, min(int(bbox[0][0][0]), frame.shape[1] - qr_width))
            top_left_y = max(0, min(int(bbox[0][0][1]), frame.shape[0] - qr_height))

            frame[top_left_y:top_left_y + qr_height, top_left_x:top_left_x + qr_width] = img_resized

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
