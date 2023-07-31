import barcode
from barcode import Code128
from barcode.writer import ImageWriter

from PIL import Image, ImageDraw, ImageFont

def create_card(data):
    # Create a blank card with a white background
    def generate_barcode(data):
        # Create the barcode object
        barcode_class = Code128(data["first_name"], writer=ImageWriter(), add_checksum=False)

        # Save the barcode as an image
        barcode_path = 'barcode.png'
        barcode_class.save(barcode_path)

        return barcode_path
    barcode_path=generate_barcode(data)
    card_width, card_height = 400, 200
    card = Image.new('RGB', (card_width, card_height), color='white')
    draw = ImageDraw.Draw(card)

    # Add the barcode image to the card
    barcode_image = Image.open(barcode_path)
    card.paste(barcode_image, (50, 50))

    # Add other information to the card
    font = ImageFont.truetype("arial.ttf", 20)
    draw.text((150, 50), f"No: {data['membership_no']}", fill='black', font=font)
    draw.text((150, 80), f"Name: {data['first_name']}", fill='black', font=font)
    draw.text((150, 110), f"Phone: {data['phone_number']}", fill='black', font=font)

    # Save the card as an image
    card_path = 'card.png'
    card.save(card_path)

    return card_path



