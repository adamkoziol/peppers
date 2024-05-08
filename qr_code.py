import argparse
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

class QRCodeGenerator:
    """
    A class used to generate a QR code with a custom logo.

    ...

    Attributes
    ----------
    data : str
        a string representing the data to be encoded in the QR code
    logo_path : str
        a string representing the path to the logo image
    output_path : str
        a string representing the path to the output image
    title : str
        a string representing the title to be printed at the top of the QR code

    Methods
    -------
    generate_qr_code():
        Generates the QR code, scales the logo, pastes the logo onto the QR
        code, and saves the image.
    """

    def __init__(self, data, logo_path, output_path, title):
        """
        Constructs all the necessary attributes for the QRCodeGenerator object.

        Parameters
        ----------
            data : str
                the data to be encoded in the QR code
            logo_path : str
                the path to the logo image
            output_path : str
                the path to the output image
            title : str
                the title to be printed at the top of the QR code
        """

        self.data = data
        self.logo_path = logo_path
        self.output_path = output_path
        self.title = title

    def generate_qr_code(self):
        """
        Generates the QR code, scales the logo, pastes the logo onto the QR
        code, and saves the image.
        """

        # Create qr code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        # Add data to qr code
        qr.add_data(self.data)

        qr.make(fit=True)

        # Create an image from the QR Code instance
        img = qr.make_image(fill='black', back_color='white')

        # Open the logo image
        logo = Image.open(self.logo_path)

        # Calculate dimensions of logo and QR code
        logo_width = logo.size[0]
        logo_height = logo.size[1]
        qr_width = img.size[0]
        qr_height = img.size[1]

        # Scale logo
        scale_factor = min(
            qr_width / logo_width, qr_height / logo_height
        ) / 3.5
        new_width = int(logo_width * scale_factor)
        new_height = int(logo_height * scale_factor)
        logo = logo.resize((new_width, new_height))

        # Calculate position for logo
        x = (qr_width - new_width) // 2
        y = (qr_height - new_height) // 2

        # Paste logo onto QR code
        img.paste(logo, (x, y))

        # Create draw object
        draw = ImageDraw.Draw(img)

        # Load font
        font = ImageFont.truetype("fonts/ttf/DejaVuSans-Bold.ttf", 30)

        # Calculate width of the title
        title_width = draw.textlength(self.title, font=font)

        # Calculate position for title
        title_x = (qr_width - title_width) // 2
        title_y = 0

        # Draw title
        draw.text((title_x, title_y), self.title, font=font, fill="black")

        # Save it somewhere, change the extension as needed:
        img.save(self.output_path)  # png, jpg, svg, pdf
        print('Saving file:', self.output_path)


# Create argument parser
parser = argparse.ArgumentParser(
    description='Generate a QR code with a custom logo.'
)
parser.add_argument(
    '--url',
    help='The URL to be encoded in the QR code.'
)
parser.add_argument(
    '--output_path',
    default='qr_codes',
    help='The output file path.'
)
parser.add_argument(
    '--output_name',
    required=True,
    help='The output file name.'
)
parser.add_argument(
    '--logo',
    default='docs/images/logo.png',
    help='The logo file name and path.'
)
parser.add_argument(
    '--title',
    required=True,
    help='The title to be printed at the top of the QR code.'
)

# Parse arguments
args = parser.parse_args()

# Create output file path
output_file_path = os.path.join(args.output_path, args.output_name)

# Create QRCodeGenerator instance and generate QR code
qr_generator = QRCodeGenerator(
    args.url,
    args.logo,
    output_file_path,
    args.title
)
qr_generator.generate_qr_code()
