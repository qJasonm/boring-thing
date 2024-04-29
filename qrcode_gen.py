import qrcode
from PIL import Image

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Add data - Website's URL
qr.add_data("bear.qjasonma.com/Lairo'thebear")
qr.make(fit=True)

# Create QR code base
img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')

# Open the overlay image
overlay_img = Image.open('bear.jpg')

# Calculate dimensions
img_w, img_h = img_qr.size
logo_size = min(img_w, img_h)
fifteen_percent_of_original = int(logo_size * 0.15) # reducing the size

# Resize the overlay image
overlay_img = overlay_img.resize((fifteen_percent_of_original, fifteen_percent_of_original))

# Calculate position for overlay image
logo_pos = (img_w // 2 - fifteen_percent_of_original // 2, img_h // 2 - fifteen_percent_of_original // 2)

# Paste overlay image at the center
img_qr.paste(overlay_img, logo_pos)

# Save qr code
img_qr.save("qr_with_bear.png")