from pyzbar.pyzbar import decode
from PIL import Image

img = Image.open('test_qr.png')

result = decode(img)

for code in result:
    qr_data = code.data.decode('utf-8')
    print(qr_data)