from PIL import Image, ImageDraw
import os

def create_app_icon():
    # Create a 256x256 image with a transparent background
    img = Image.new('RGBA', (256, 256), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define colors
    primary_color = (74, 111, 165)  # #4a6fa5 - Blue
    secondary_color = (107, 142, 35)  # #6b8e23 - Olive green
    
    # Draw a rounded rectangle for the background
    draw.rectangle([20, 20, 236, 236], fill=primary_color, outline=None, width=0)
    
    # Draw a network/proxy icon
    # Center circle
    draw.ellipse([88, 88, 168, 168], outline="white", width=8)
    
    # Connection lines
    # Top
    draw.line([128, 40, 128, 88], fill="white", width=8)
    # Bottom
    draw.line([128, 168, 128, 216], fill="white", width=8)
    # Left
    draw.line([40, 128, 88, 128], fill="white", width=8)
    # Right
    draw.line([168, 128, 216, 128], fill="white", width=8)
    
    # Corner nodes
    draw.ellipse([30, 30, 50, 50], fill=secondary_color)
    draw.ellipse([206, 30, 226, 50], fill=secondary_color)
    draw.ellipse([30, 206, 50, 226], fill=secondary_color)
    draw.ellipse([206, 206, 226, 226], fill=secondary_color)
    
    # Save the image as ICO file
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    img.save('assets/proxy_manager_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print("Icon created successfully at 'assets/proxy_manager_icon.ico'")
    return 'assets/proxy_manager_icon.ico'

if __name__ == "__main__":
    create_app_icon()