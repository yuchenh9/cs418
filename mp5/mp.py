import copy
import sys
import numpy
import math
from PIL import Image
from triclip import *

sun=[-1,-1,-1]
png_width=-1
png_height=-1
png_name=""
sphere_xs=[]
sphere_ys=[]
sphere_zs=[]
sphere_rs=[]
if len(sys.argv) < 2:
    print("Usage: python your_program.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
try:
    with open(input_file, 'r') as file:
        input_string = file.read()

        # Split the input string into lines
        lines = input_string.splitlines()
        current_color=(255,255,255,255)
        # Trim leading and trailing spaces for each parsed string
        for line in lines:
            line=line.strip()
            newwords=line.split()
            newwords = [word.strip() for word in newwords]
            if len(newwords)==0:
                continue
            if newwords[0]=='png' :
                png_width=int(newwords[1])
                png_height=int(newwords[2])
                png_name=newwords[3]
            if newwords[0]=='sphere' :
                sphere_x=float(newwords[1])
                sphere_y=float(newwords[2])
                sphere_z=float(newwords[3])
                sphere_r=float(newwords[4])
                sphere_xs.append(sphere_x)
                sphere_ys.append(sphere_y)
                sphere_zs.append(sphere_z)
                sphere_rs.append(sphere_r)
            
            if newwords[0]=='sun' :
                sun_x=float(newwords[1])
                sun_y=float(newwords[2])
                sun_z=float(newwords[3])
        #