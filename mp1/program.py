
import sys
from PIL import Image

# ...
#image = Image.new("RGBA", (width, height), (0,0,0,0))
# ...
#image.im.putpixel((x,y), (red, green, blue, alpha))
# ...
#image.save(filename)


if len(sys.argv) < 2:
    print("Usage: python your_program.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
words = []
try:
    with open(input_file, 'r') as file:
        input_string = file.read()

        # Split the input string into lines
        lines = input_string.splitlines()
        
        # Trim leading and trailing spaces for each parsed string
        for line in lines:
            line=line.strip()
            newwords=line.split()
            newwords = [word.strip() for word in newwords]
            if len(newwords)==0:
                continue
            if newwords[0]=='png' :
                image = Image.new("RGBA", (int(newwords[1]), int(newwords[2])), (0,0,0,0))
                name=newwords[]
            if newwords[0]=='xyrgb' :
                image.im.putpixel((int(newwords[1]),int(newwords[2])), (int(newwords[3]),int(newwords[4]),int(newwords[5]),255))
            if newwords[0]=='xyc' :
                red = int(newwords[3][1:3], 16)
                green = int(newwords[3][3:5], 16)
                blue = int(newwords[3][5:7], 16)
                image.im.putpixel((int(newwords[1]),int(newwords[2])),(red,green,blue,255))
            #words.extend(newwords)
        image.save('b.png')

       
except FileNotFoundError:
    print("Input file not found.")
except IOError:
    print("Error reading the input file.")