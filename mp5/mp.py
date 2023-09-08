import copy
import sys
import numpy
import math
from PIL import Image
#from triclip import *

def _max(a,b):
    if a>b:
        return a
    else :
        return b
sun=[-1,-1,-1]
png_width=-1
png_height=-1
png_name=""
sphere_xs=[]
sphere_ys=[]
sphere_zs=[]
sphere_rs=[]
##collision_detection(ray,each_sphere,result_list_to_append_to)：
    #v3 d1=(sphere_center-ray_origin)
    #inside=d1*(dot)d1 < sphere_r**2
    #v3 ray_direction=normalized(ray_direction)
    #v1 tc=d1*(dot)ray_direction
    #if inside==False and tc<0:
    #   return
    #v3 d2=ray_origin+tc*ray_direction-sphere_center
    #hit=sphere_r**2-d2*(dot)d2>0
    #if hit==False:
    #   return
    #v1 d3=sqrt(sphere_r**2-d2**2)
    #if inside:
    #   v1 d=tc+d3
    #else:
    #   v1 d=tc-d3
    #result_list_to_append_to.append:d;sphere_index
def collision_detection(ray,sphere_index,toAppend):
    ray_origin,ray_direction=ray
    sphere_center=[sphere_xs[sphere_index],sphere_ys[sphere_index],sphere_zs[sphere_index]]
    sphere_r=sphere_rs[sphere_index]
    sphere_center=numpy.array(sphere_center)
    ray_origin=numpy.array(ray_origin)
    ray_direction=numpy.array(ray_direction)
    ray_direction=ray_direction / numpy.linalg.norm(ray_direction)
    #print(ray_direction)
    d1=sphere_center-ray_origin
    inside=numpy.dot(d1,d1)<sphere_r**2
    tc=numpy.dot(d1,ray_direction)
    if inside==False and tc<0:
        return
    d2=ray_origin+numpy.dot(tc,ray_direction)-sphere_center
    hit=(sphere_r**2-numpy.dot(d2,d2))>0
    if hit==False:
        return
    d3=(sphere_r**2-numpy.dot(d2,d2))**(1/2)
    d=0.0
    if inside:
        d=tc+d3
    else:
        d=tc-d3
    toAppend[sphere_index]=d
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
                sun_xs.append(sun_x)
                sun_ys.append(sun_y)
                sun_zs.append(sun_z)
        
        image = Image.new("RGBA", (png_width,png_height), (255,255,255,255))
        for x in range(png_width):
            for y in range(png_height):
                _x=(2*x-png_width)/max(png_width,png_height)
                _y=(2*y-png_height)*(-1)/max(png_width,png_height)
                ray_direction=[_x,_y,-1]
                ray_origin=[0,0,0]
                ##v3 ray_direction=normalized(ray_direction)
                ##v3 d1=(sphere_center-ray_origin)
                ##v3 d2=ray_origin+tc*ray_direction-sphere_center
                ##v1 d3=sqrt(sphere_r**2-d2**2)
                collision_list={}
                for sphere_index in range(len(sphere_xs)):
                    ray=[ray_origin,ray_direction]
                    collision_detection(ray,sphere_index,collision_list)
                rgb=[]
                    #print(collision_list)
                if collision_list!={}:
                    image.im.putpixel((x,y),(0,0,0,255))
                #larger than zero, least d1 sphere
                #
        
        image.save('bug.png')
except BaseException: 
    print("shit!")
finally:
    print("ok")
                    