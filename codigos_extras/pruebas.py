# Crear un QR
# qr = qrcode.QRCode(
#     version=1,
#     error_correction=qrcode.constants.ERROR_CORRECT_L,
#     box_size=10,
#     border=4,
# )
# qr.add_data('https://www.google.com')
# qr.make(fit=True)

# img = qr.make_image(fill_color="black", back_color="white")
# img.save('qr.png')

from qreader import QReader
import cv2


# Create a QReader instance
qreader = QReader()

# Get the image that contains the QR code
image = cv2.cvtColor(cv2.imread("qr.png"), cv2.COLOR_BGR2RGB)

# Use the detect_and_decode function to get the decoded QR data
decoded_text = qreader.detect(image=image)
print(decoded_text[0].quad_xy)