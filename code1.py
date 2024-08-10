from PIL import Image, ImageDraw
import qrcode
import numpy as np
import math

def create_circular_qr_overlay(input_image_path, output_image_path, qr_data="https://example.com"):
    # Open the input image
    base_image = Image.open(input_image_path).convert("RGB")
    width, height = base_image.size

    # Create a QR code
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Create QR code image
    qr_image = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    qr_width, qr_height = qr_image.size

    # Resize input image to match QR code size
    base_image = base_image.resize((qr_width, qr_height), Image.LANCZOS)

    # Create circular mask
    mask = Image.new('L', (qr_width, qr_height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, qr_width, qr_height), fill=255)

    # Convert images to numpy arrays
    base_array = np.array(base_image)
    qr_array = np.array(qr_image)
    mask_array = np.array(mask)

    # Create dotted pattern for QR code
    dot_size = 3
    dot_space = 2
    for i in range(0, qr_width, dot_size + dot_space):
        for j in range(0, qr_height, dot_size + dot_space):
            if np.all(qr_array[j:j+dot_size, i:i+dot_size] == 0):
                base_array[j:j+dot_size, i:i+dot_size] = [0, 0, 0]

    # Apply circular mask
    alpha = 0.3  # Adjust this value to change the blend strength
    blended = base_array * (1 - alpha) + qr_array * alpha
    result_array = np.where(mask_array[:,:,np.newaxis] == 255, blended, base_array)

    # Convert back to image
    result_image = Image.fromarray(result_array.astype('uint8'), 'RGB')

    # Save the result
    result_image.save(output_image_path)

# Usage
input_image = "image.jpg"
output_image = "image.png"
create_circular_qr_overlay(input_image, output_image, "https://example.com")