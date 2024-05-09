#! /usr/env/python 3

"""
Generate custom QR codes. Outputs single images, and 4 x 5 tiled
"""

# Standard imports
import argparse
import csv
import os

# Third party imports
from PIL import (
    Image,
    ImageDraw,
    ImageFont
)
import qrcode


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

        # Draw email at the bottom
        email = "canaanlea.farm@gmail.com"
        email_width = draw.textlength(email, font=font)
        email_x = (qr_width - email_width) // 2
        email_y = qr_height - 40  # adjust as needed
        draw.text((email_x, email_y), email, font=font, fill="black")

        # Save single QR code
        single_output = f'{self.output_path}_single.png'
        img.save(single_output)  # png, jpg, svg, pdf
        print('Saving file:', single_output)

        # Function to convert cm to pixels
        def cm_to_pixels(cm):
            return int(cm * 118.11)  # 1 cm = 118.11 pixels at 300 DPI

        # Scale QR code to approximately 5 cm x 5 cm (assuming 300 DPI)
        scaled_img = img.resize((cm_to_pixels(5), cm_to_pixels(5)))

        # Create new image for tiling
        spacing = cm_to_pixels(0.5)  # 1 cm spacing
        tile_width = scaled_img.width * 4
        tile_height = (scaled_img.height + spacing) * 5
        tiled_img = Image.new('RGB', (tile_width, tile_height), 'white')

        # Paste QR codes into tiled image
        for i in range(5):
            for j in range(4):
                tiled_img.paste(
                    scaled_img,
                    (j * scaled_img.width, i * (scaled_img.height + spacing))
                )

        # Save tiled QR code
        tiled_output = f'{self.output_path}_tiled.png'
        tiled_img.save(tiled_output)
        print('Saving file:', tiled_output)


# Create argument parser
parser = argparse.ArgumentParser(
    description='Generate a QR codes with a custom logo.'
)
parser.add_argument(
    '--file',
    help='The file containing the titles and output names.'
)
parser.add_argument(
    '--url',
    help='The URL to be encoded in the QR code.'
)
parser.add_argument(
    '--output_path',
    default='QR_codes',
    help='The output file path.'
)
parser.add_argument(
    '--output_name',
    help='The output file name.'
)
parser.add_argument(
    '--logo',
    default='docs/images/logo.png',
    help='The logo file name and path.'
)
parser.add_argument(
    '--title',
    help='The title to be printed at the top of the QR code.'
)

# Parse arguments
args = parser.parse_args()

if args.file:
    # Read from file
    with open(args.file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            title, output_name = row

            # Construct URL
            url = f'https://adamkoziol.github.io/peppers/{output_name}'

            # Create output file path
            output_file_path = os.path.join(
                args.output_path,
                output_name)
            # Create QRCodeGenerator instance and generate QR code
            qr_generator = QRCodeGenerator(
                url,
                args.logo,
                output_file_path,
                title
            )
            qr_generator.generate_qr_code()
else:
    # Check if url, output_name and title are provided
    if not all([args.url, args.output_name, args.title]):
        print("Please provide url, output_name and title arguments.")
        raise SystemExit

    # Create output file path
    output_file_path = os.path.join(
        args.output_path,
        args.output_name)

    # Create QRCodeGenerator instance and generate QR code
    qr_generator = QRCodeGenerator(
        args.url,
        args.logo,
        output_file_path,
        args.title
    )
    qr_generator.generate_qr_code()
