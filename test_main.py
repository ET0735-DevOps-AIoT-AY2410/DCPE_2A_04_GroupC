from PIL import Image, ImageDraw, ImageFont
from pyzbar.pyzbar import decode

# Use raw strings for file paths to avoid invalid escape sequences
image_path = r'C:\Local_Git_Repository\CA\DCPE_2A_04_GroupC\helloworld.png'
font_path = r'C:\Windows\Fonts\Arial.ttf'  # Adjust this path to where Arial.ttf is located

try:
    # Open an image file
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    # Load a font
    font = ImageFont.truetype(font_path, size=20)  # Ensure the correct path to Arial.ttf

    # Decode any barcodes in the image
    for d in decode(img):
        # Draw a rectangle around the detected barcode
        draw.rectangle(
            ((d.rect.left, d.rect.top), (d.rect.left + d.rect.width, d.rect.top + d.rect.height)),
            outline=(0, 0, 255), width=3
        )
        # Draw a polygon around the detected barcode
        draw.polygon(d.polygon, outline=(0, 255, 0), width=3)
        # Draw the decoded data as text
        draw.text(
            (d.rect.left, d.rect.top + d.rect.height), d.data.decode(),
            (255, 0, 0), font=font
        )

    # Save the edited image
    img.save(image_path)
    print("Image saved successfully.")
except OSError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
