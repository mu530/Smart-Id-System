import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.contrib.staticfiles import finders


def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="#4054B2", back_color="#ffb606")

    # Find the absolute path to the logo image in the static folder
    logo_path = finders.find("image/logo.png")

    # Open and resize the logo image
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((50, 50))  # Resize the logo to 50x50 pixels

    # Calculate the position to place the logo
    qr_width, qr_height = qr_image.size
    logo_width, logo_height = logo_image.size
    logo_position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)

    # Paste the logo onto the QR code image
    qr_image.paste(logo_image, logo_position)

    buf = BytesIO()
    qr_image.save(buf, format="PNG")
    buf.seek(0)
    image = File(buf, name="qr_code_with_logo.png")
    return image
