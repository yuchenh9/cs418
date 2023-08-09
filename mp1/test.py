from PIL import Image

# Open an image file
img = Image.open('splat2.png')

# Get image dimensions
width, height = img.size
print('Width:', width)
print('Height:', height)

# Access a specific pixel
x = width-1
y = height-1
pixel = img.getpixel((x, y))

print('Pixel at (50,50):', pixel)