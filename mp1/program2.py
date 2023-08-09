import copy
import sys
import numpy
import math
from PIL import Image
from triclip import *
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
x=[]
y=[]
z=[]
w=[]
x_viewport=[]
y_viewport=[]
r=[]
g=[]
b=[]
a=[]
tri=[]
hyp=False
def getPerspectiveMatrix():
    a=1
    theta=math.pi/2
    n=0.1
    f=10
    t=n*math.tan(theta/2)
    b=-t
    r=a*t
    l=-r
    perspective_matrix=numpy.array([
    [2*n/(r-l),0,0,0],
    [0,2*n/(t-b),0,0],
    [0,0,(f+n)/(f-n),-2*f*n/(f-n)],
    [0,0,1,0]
    ])
    return perspective_matrix

def getPointsByValue(up,low):
    dx=up[0]-low[0]
    dy=up[1]-low[1]
    dz=up[2]-low[2]
    #print(f'{dx},{dy},{dz}')
    if dy==0 :

        return []
    dx=dx/dy
    dz=dz/dy
    dy=1
    oy=math.ceil(low[1])-low[1]
    ox=oy*dx
    oz=oy*dz
    newy=oy+low[0]
    newx=ox+low[1]
    newz=oz+low[2]
    toreturn=[]
    
    while newy<up[1]:
        toreturn.append((newx,newy,newz))
        newx=newx+dx
        newy=newy+dy
        newz=newz+dz
    return toreturn
def getPoints(up_index,low_index):
    dx=x_viewport[up_index]-x_viewport[low_index]
    #print(up_index)
    #print(low_index)
    dy=y_viewport[up_index]-y_viewport[low_index]
    #dz=z_viewport[up_index]-z_viewport[low_index]
    if dy==0 :
        return []
    dx=dx/dy
    #dz=dz/dy
    dy=1
    oy=math.ceil(y_viewport[low_index])-y_viewport[low_index]
    ox=oy*dx
    #oz=oy*dz
    newy=oy+y_viewport[low_index]
    newx=ox+x_viewport[low_index]
    
    
    toreturn=[]
    
    while newy<y_viewport[up_index]:
        toreturn.append((newx,newy))
        newx=newx+dx
        newy=newy+dy
        #newz=newz+dz
    #print(toreturn)
    return toreturn
def viewPort(x,y,w,width,height):
    return ((x/w+1)*width/(2),(y/w+1)*height/(2))
def getLerpLinear(l,m,u,p):
    lu=[u[0]-l[0],u[1]-l[1]] #w1 x
    lm=[m[0]-l[0],m[1]-l[1]] #w2 y
    a=numpy.array([[lu[0],lm[0]],[lu[1],lm[1]]])
    #print(f'{l},{m},{u},{p}')
    #print(a)
    lp=[p[0]-l[0],p[1]-l[1]]
    b=numpy.array(lp)
    #print(b)
    return numpy.linalg.solve(a,b)

def getLerpLinearUnit(l,m,u):
    x=numpy.array([1,0])
    y=numpy.array([0,1])
    lu=[u[0]-l[0],u[1]-l[1]] #w1 x
    lm=[m[0]-l[0],m[1]-l[1]] #w2 y
    a=numpy.array([[lu[0],lm[0]],[lu[1],lm[1]]])
    #print(f'{l},{m},{u},{p}')
    #print(a)
    #print(b)
    return (numpy.linalg.solve(a,x),numpy.linalg.solve(a,y))

def sRGB_to_linear(color):
    linear_color = []
    for value in color:
        normalized_value = value / 255.0
        if normalized_value <= 0.04045:
            linear_value = normalized_value / 12.92
        else:
            linear_value = ((normalized_value + 0.055) / 1.055) ** 2.4
        linear_color.append(linear_value)
    return linear_color
def linear_to_sRGB(color):
    sRGB_color = []
    for value in color:
        if value <= 0.0031308:
            sRGB_value = int(value * 12.92 * 255 + 0.5)
        else:
            sRGB_value = int((1.055 * (value**(1 / 2.4)) - 0.055) * 255 + 0.5)
        sRGB_color.append(sRGB_value)
    return sRGB_color
#mats  primitive->#clip->#[x,y,z,w]*=1/w->perspectiveproject[x,y,z,1]->viewport->(draw)hypinterpolation->

def getColor(up_index,low_index):
    Dx=x_viewport[up_index]-x_viewport[low_index]
    #print(up_index)
    #print(low_index)
    Dy=y_viewport[up_index]-y_viewport[low_index]
    

    dx=Dx/Dy
    dy=1
    oy=math.ceil(y_viewport[low_index])-y_viewport[low_index]
    ox=oy*dx
    newy=oy+y_viewport[low_index]
    newx=ox+x_viewport[low_index]
    dcolor=((r[up_index] -r[low_index] )/Dy,(g[up_index] -g[low_index] )/Dy,(b[up_index] -b[low_index] )/Dy,0)
    color=(r[low_index] ,g[low_index] ,b[low_index] ,255)
    toreturn=[]
    
    while newy<y_viewport[up_index]:
        toreturn.append(color)
        color=(color[0]+dcolor[0],color[1]+dcolor[1],color[2]+dcolor[2],255)
        newx=newx+dx
        newy=newy+dy
    return toreturn
def draw(tri):
    if tri[0]==-1:
        return
    up_index=tri[0]
    low_index=tri[0]
    middle_index=tri[0]
    #print(tri)
    #print(f'up:{up_index},middle:{middle_index},low:{low_index}')
    #print(f'len(y_v):{len(y_viewport)}')
    for a in tri:
        #print(f'up_index={up_index},aaa={a}')
        if y_viewport[up_index]<y_viewport[a]:
            up_index=a
        if y_viewport[a]<y_viewport[low_index]:
            low_index=a
    for a in tri:
        if a!=low_index and a!=up_index:
            middle_index=a
    #print(f'up_index={up_index},middle_index={middle_index},low_index={low_index}')
    line_a=getPoints(up_index,low_index)
    line_b=getPoints(middle_index,low_index)+getPoints(up_index,middle_index)
    if len(line_a)==0 or len(line_b)==0:
        return
    #print(a)
    #print(f'len a = {len(a)},len b ={len(b)}')
    #return
    direction=1
    if line_a[1][0]>=line_b[1][0]:
        direction=-1
    #get the first integer point in the triangle
    #if direction==1:
    #    _x=math.ceil(line_a[0][0])#
    #else :
    #    _x=math.floor(line_a[0][0])#
    #_y=line_a[0][1]
    #first_point=(_x,_y)
    #op=(_x-x[up_index],_y-y[up_index])
    #print(f'''low:{(x_viewport[low_index],y_viewport[low_index])},
    #        middle:{(x_viewport[middle_index],y_viewport[middle_index])},
    #        up:{(x_viewport[up_index],y_viewport[up_index])},
    #        ''')
    #print(f'''low:{(x[low_index],y[low_index])},
    #middle:{(x[middle_index],y[middle_index])},
    #up:{(x[up_index],y[up_index])},
    #''')
    basedepth=z[low_index]
    W1_z=z[up_index]-basedepth
    W2_z=z[middle_index]-basedepth
    base_w=w[low_index]
    W1_w=w[up_index]-base_w
    W2_w=w[middle_index]-base_w
    basecolor=(r[low_index],g[low_index]  ,b[low_index] ,255)
   #print(f'{r[up_index]-r[low_index]},{g[up_index]-g[low_index]},{b[up_index]-b[low_index]}')
    W1=(r[up_index]-r[low_index],g[up_index]-g[low_index],b[up_index]-b[low_index] ,0)
    W2=(r[middle_index] -r[low_index] ,g[middle_index] -g[low_index] ,b[middle_index] -b[low_index] ,0)
    #(unit_x,unit_y)=getLerpLinearUnit((x_viewport[low_index],y_viewport[low_index]),(x_viewport[middle_index],y_viewport[middle_index]),(x_viewport[up_index],y_viewport[up_index]))
    #print(f'{unit_x},{unit_y}')
    for i in range(len(line_a)):
        ax=line_a[i][0]
        bx=line_b[i][0]
        #print(f'ax={ax},bx={bx}')
        #dcolor=(bcolor[i][0]-acolor[i][0],bcolor[i][1]-acolor[i][1],bcolor[i][2]-acolor[i][2],0)
        dx=(line_b[i][0]-line_a[i][0])*direction
        #if dx==0:
        #    dcolor=(0,0,0,0)
        #else:
        #    dcolor=(dcolor[0]/dx,dcolor[1]/dx,dcolor[2]/dx,0)
        #color=(acolor[i][0],acolor[i][0],acolor[i][0],255)
        if direction==1:
            x_value=math.ceil(ax)#
            condition=x_value < bx and x_value>=0 and x_value<=width and line_a[i][1]>=0 and line_a[i][1]<=height
        else :
            x_value=math.floor(ax)#
            condition=x_value >= bx   and x_value>=0 and x_value<=width and line_a[i][1]>=0 and line_a[i][1]<=height

        dif=x_value-ax
        p=(ax+dif,line_a[i][1])
        #print(p)
        #print(f'line y={a[i][1]} x={a[i][0]} -- {b[i][0]}') 
        while condition:#
            #print((int(x_value),int(a[1])))
            #print((x_value))
            if x_value> width or line_a[i][1]>height :
                x_value=x_value+direction
                if direction==1:
                    condition=x_value < line_b[i][0]
                else:
                    condition=x_value >= line_b[i][0]                                
                p=(p[0]+direction,p[1])
                break
                
            if x_value== width or line_a[i][1]==height :
                x_value=x_value+direction
                if direction==1:
                    condition=x_value < line_b[i][0]
                else:
                    condition=x_value >= line_b[i][0]                                
                p=(p[0]+direction,p[1])
                continue
           #print(f'{(x_viewport[low_index],y_viewport[low_index])},{(x_viewport[middle_index],y_viewport[middle_index])},{(x_viewport[up_index],y_viewport[up_index])},{p}')
            
            (w1,w2)=getLerpLinear((x_viewport[low_index],y_viewport[low_index]),(x_viewport[middle_index],y_viewport[middle_index]),(x_viewport[up_index],y_viewport[up_index]),p)
            
            #dif_x=_x-first_point[0]
            #dif_y=_y-first_point[1]
            #(w1,w2)=((op[0]+dif_x)*unit_x[0]+(op[1]+dif_y)*unit_y[0],(op[0]+dif_x)*unit_x[1]+(op[1]+dif_y)*unit_y[1])
           
            _depth=basedepth+W1_z*w1+W2_z*w2
            _w=base_w+W1_w*w1+W2_w*w2
            _x=round(x_value)
            _y=round(line_a[i][1])

            
            _r=basecolor[0]+W1[0]*w1+W2[0]*w2
            _g=basecolor[1]+W1[1]*w1+W2[1]*w2
            _b=basecolor[2]+W1[2]*w1+W2[2]*w2
            if hyp:
                _r=_r/_w
                _g=_g/_w
                _b=_b/_w
            #print(f'_x={_x},_y={_y}')
            if depth_flag==False:
                #image.im.putpixel((_x,_y),(round(255*_r),round(255*_g),round(255*_b),255))
                pixels[_y][_x]=[(_r),(_g),(_b),1]
            else:
                #print(f'_x={_x},_y={_y}')
                if _depth<=pixel_depth[_y][_x] and _depth>=-1:
                    #print("yes")
                    pixel_depth[_y][_x]=_depth
                    #print(pixel_depth[round(x_value)][round(a[i][1])])
                    #image.im.putpixel((_x,_y),(round(255*_r),round(255*_g),round(255*_b),255))
                    pixels[_y][_x]=[(_r),(_g),(_b),1]
            print(f'rgb={_r},{_g},{_b}')
            x_value=x_value+direction
            if direction==1:
                condition=x_value < line_b[i][0]
            else:
                condition=x_value >= line_b[i][0]                                
            p=(p[0]+direction,p[1])
def linearTosRGB(color):
        if color <= 0.0031308:
            return color * 12.92
        else:
            return 1.055 * (color ** (1 / 2.4)) - 0.055
def sRGBToLinear(color):
    if color <= 0.04045:
        return color / 12.92
    else:
        return ((color + 0.055) / 1.055) ** 2.4

depth_flag=False
sRGB=False
frustum=False
cull=False
fsaa=0
clipping_mats=numpy.array([[1,0,0,1],[-1,0,0,1],[0,1,0,1],[0,-1,0,1],[0,0,1,1],[0,0,-1,1]])
tris=[]
pixels=[]
planes=[]
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
                original_width=int(newwords[1])
                original_height=int(newwords[2])
                name=newwords[3]
            if newwords[0]=='sRGB' :
                sRGB=True
            if newwords[0]=='cull':
                cull=True
            if newwords[0]=='clipplane':
                clipplane=[float(newwords[1]),float(newwords[2]),float(newwords[3]),float(newwords[4])]
                planes.append(clipplane)
            if newwords[0]=='xyzw' :
                _x=float(newwords[1])
                _y=float(newwords[2])
                _z=float(newwords[3])
                _w=float(newwords[4])
                x.append(_x)
                y.append(_y)
                z.append(_z)
                w.append(_w)
                r.append(current_color[0]/255)
                g.append(current_color[1]/255)
                b.append(current_color[2]/255)
            if newwords[0]=='rgb' :
                current_color=(int(newwords[1]),int(newwords[2]),int(newwords[3]),current_color[-1])
            if newwords[0]=='frustum':
                frustum=True
            if newwords[0]=='fsaa':
                fsaa=int(newwords[1])
            if newwords[0]=='depth':
                depth_flag=True
            
            if newwords[0]=='hyp':
                hyp=True
                
            if newwords[0]=='tri' :
                tri=[]
                for element in newwords[1:4]:
                    element=int(element)
                    if element>0:
                        tri.append(element-1)
                    else :
                        if element<0:
                            tri.append(len(x)+element)
                #tri=[int(element)-1 if int(element)>0 else len(tri)+int(element) if len(tri)>0 else 3+int(element) for element in newwords[1:4]]
                tris.append(tri)
                #print(f"append{tri}")
                #draw(tri)
    if fsaa>0:
        width=original_width*fsaa
        height=original_height*fsaa
    else:
        width=original_width
        height=original_height
    image = Image.new("RGBA", (original_width,original_height), (255,255,255,255))
    pixel_depth=[[10] * width for _ in range(height)]
    pixels=[[0,0,0,0] * width for _ in range(height)]
    if cull:
        index=0
        for tri in tris:
            seg_a=[x[tri[1]]-x[tri[0]],y[tri[1]]-y[tri[0]]]
            seg_b=[x[tri[2]]-x[tri[1]],y[tri[2]]-y[tri[1]]]
            if numpy.cross(seg_a, seg_b)>0:
                tris[index][0]=-1
            index+=1
    if frustum:
        planes.append(numpy.array([1,0,0,1]))
        planes.append(numpy.array([-1,0,0,1]))
        planes.append(numpy.array([0,1,0,1]))
        planes.append(numpy.array([0,-1,0,1]))
        planes.append(numpy.array([0,0,1,1]))
        planes.append(numpy.array([0,0,-1,1]))
    for plane in planes:
        for i in range(len(tris)):
            if tris[i][0]==-1:
                continue
            clip_and_append_xsyszs_and_tris(plane,i,tris,x,y,z,w,r,g,b)
    #print(w)
    for i in range(len(x)):
        if(w[i]==0.0):
            x_viewport.append(0)
            y_viewport.append(0)#this value is not going to be used
            continue
        (_x,_y)=viewPort(x[i],y[i],w[i],width,height)
        x_viewport.append(_x)
        y_viewport.append(_y)
    if sRGB:
        for i in range(len(x)):
            r[i]=sRGBToLinear(r[i])
            g[i]=sRGBToLinear(g[i])
            b[i]=sRGBToLinear(b[i])
    if hyp:
        for i in range(len(x)):
            r[i]=r[i]/w[i]
            g[i]=g[i]/w[i]
            b[i]=b[i]/w[i]
            w[i]=1/w[i]
            
    #print(f'before draw(){pixels[4]}')
    for tri in tris:
        draw(tri)
        #print(f'i draw {tri}')
        #for i in [up_index,middle_index,low_index]:
        #    print(f'({x[i]},{y[i]})')
        base=[0,0,0,0]
    

    pixels_after_fsaa=copy.deepcopy(pixels)
    for x in range(original_width):
        for y in range(original_height):
            if sRGB or fsaa>0:
                _r=linearTosRGB(pixels_after_fsaa[y][x][0])
                _g=linearTosRGB(pixels_after_fsaa[y][x][1])
                _b=linearTosRGB(pixels_after_fsaa[y][x][2])
                _a=linearTosRGB(pixels_after_fsaa[y][x][3])
                #print((_r,_g,_b))
            else:
                _r=pixels_after_fsaa[y][x][0]
                _g=pixels_after_fsaa[y][x][1]
                _b=pixels_after_fsaa[y][x][2]
                _a=pixels_after_fsaa[y][x][3]
            image.im.putpixel((x,y),(round(255*_r),round(255*_g),round(255*_b),round(255*_a)))
    image.save(name)
    for x in range(original_width):
        for y in range(original_height):
            for i in range(4):
                pixels_after_fsaa[y][x][i]=round(255*pixels_after_fsaa[y][x][i])
    with open('output2.txt', 'w') as f:
        # Iterate over each sublist in the 2D array
        for sublist in pixels:
            # Convert each item in the sublist to a string, then join them with commas
            line = ', '.join(map(str, sublist))
            # Write the line to the file, followed by a newline
            f.write(line + '\n')
except FileNotFoundError:
    print("Input file not found.")
except IOError:
    print("Error reading the input file.")


