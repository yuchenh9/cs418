import copy
import sys
import numpy
import math
from PIL import Image
#from triclip import *
def srgb_to_linear(channel_value):
    if channel_value <= 0.04045:
        return channel_value / 12.92
    else:
        return ((channel_value + 0.055) / 1.055) ** 2.4
def tosRGB(a):
    if a<=0.0031308:
        return 12.92*a
    else:
        return 1.055*a**(1/2.4)-0.055
def _max(a,b):
    if a>b:
        return a
    else :
        return b
def clamp(a):
    if a>1:
        return 1
    if a<0:
        return 0
    return a
def getProject(a,b):
    return (numpy.dot(a, b) / numpy.dot(b, b)) * b
sun=[-1,-1,-1]
png_width=-1
png_height=-1
png_name=""
sphere_xs=[]
sphere_ys=[]
sphere_zs=[]
sphere_rs=[]
sphere_rgbs=[]
sun_rgbs=[]
sun_xs=[]
sun_ys=[]
sun_zs=[]
color=[1.0,1.0,1.0]
plane_normals=[]
plane_points=[]
plane_rgbs=[]
xyz_s=[]
xyz_coords=[]
tris=[]
tri_rgbs=[]
tri_normals=[]
tri_points=[]
tris_edge_normals=[]
texcoord =[0,0]
last_texture='none'
textures={}
bulb_xyzs=[]
bulb_colors=[]
def getBarycentric_0f_edge(point,tri_index,i):
    point=numpy.array(point)
    normal=tris_edge_normals[tri_index][i]
    unprojected_point_edge=point-numpy.array(xyz_s[tris[tri_index][(i+1)%3]])
    Bary=numpy.dot(unprojected_point_edge,normal)/numpy.dot(normal,normal)
    return Bary
def collision_detection_only(ray,self_sphere,self_tri):
    ray_origin,ray_direction=ray
    ray_origin=numpy.array(ray_origin)
    ray_direction=numpy.array(ray_direction)
    shadowed=False
    for sphere_index in range(len(sphere_rs)):
        if sphere_index==self_sphere:
            continue
        sphere_center=[sphere_xs[sphere_index],sphere_ys[sphere_index],sphere_zs[sphere_index]]
        sphere_r=sphere_rs[sphere_index]
        sphere_center=numpy.array(sphere_center)
    #print(ray_direction)
        d1=sphere_center-ray_origin
        inside=numpy.dot(d1,d1)<sphere_r**2
        tc=numpy.dot(d1,ray_direction)
        if inside==False and tc<0:
            #print("not shadowed")
            continue
        d2=ray_origin+numpy.dot(tc,ray_direction)-sphere_center
        hit=(sphere_r**2-numpy.dot(d2,d2))>0
        if hit==False:
            #print("not shadowed")
            continue
        #print(f"collide with {sphere_index}")
        return True
    for tri_index in range(len(tri_rgbs)):
        if tri_index==self_tri:
            continue
        _normal=tri_normals[tri_index]
        #print(ray_direction)
        if numpy.dot(ray_direction,_normal)==0:
            #print(f'zer0!{ray_direction}*{_normal}')
            continue
        t=numpy.dot((numpy.array(xyz_s[tri_points[tri_index]])-numpy.array(ray_origin)),_normal)/numpy.dot(ray_direction,_normal)
        #print(f't={t}')
        if t<0:
            continue
        hit_position=ray_origin+t*ray_direction
        Barys=[]
        Bary_sums=0
        outside=False
        for i in range(3):
            v=getBarycentric_0f_edge(hit_position,tri_index,i)
            if v<1e-10 :
                outside=True
                continue
        if outside:
            continue
        return True
    return False
def planes_collision_detection(ray,plane_index,toAppend):
    ray_origin,ray_direction=ray
    ray_direction=ray_direction/numpy.linalg.norm(ray_direction)
    ray_origin=numpy.array(ray_origin)
    _normal=plane_normals[plane_index]
    #print(ray_direction)
    if numpy.dot(ray_direction,_normal)==0:
        #print(f'zer0!{ray_direction}*{_normal}')
        return
    t=numpy.dot((numpy.array(plane_points[plane_index])-numpy.array(ray_origin)),_normal)/numpy.dot(ray_direction,_normal)
    if t<0:
        return
    hit_position=ray_origin+t*ray_direction
    rgb=[0,0,0]
    for sun_index in range(len(sun_xs)):
        sun_position=numpy.array([sun_xs[sun_index],sun_ys[sun_index],sun_zs[sun_index]])
        light_direction=sun_position
        light_direction=light_direction/numpy.linalg.norm(light_direction)
        
        light_position_and_direction=[hit_position,light_direction]
        if collision_detection_only(light_position_and_direction,-1,-1):
            #print(f'sphere{sphere_index} is shadowed')
            continue
        #else:
            #print(f'sphere{sphere_index} not shadowed')
        normal_dot_view=numpy.dot(_normal,light_direction)
        rgb=rgb+numpy.array([sun_rgbs[sun_index][0]*normal_dot_view*plane_rgbs[plane_index][0],
                             sun_rgbs[sun_index][1]*normal_dot_view*plane_rgbs[plane_index][1],
                             sun_rgbs[sun_index][2]*normal_dot_view*plane_rgbs[plane_index][2]])
        #rgb=rgb+numpy.array([normal_dot_view,normal_dot_view,normal_dot_view])
        #print(normal_dot_view)
    toAppend.append([plane_index,t,rgb])
def tris_collision_detection(ray,tri_index,toAppend):
    ray_origin,ray_direction=ray
    ray_direction=ray_direction/numpy.linalg.norm(ray_direction)
    ray_origin=numpy.array(ray_origin)
    _normal=tri_normals[tri_index]
    #print(ray_direction)
    if numpy.dot(ray_direction,_normal)==0:
        #print(f'zer0!{ray_direction}*{_normal}')
        return
    t=numpy.dot((numpy.array(xyz_s[tri_points[tri_index]])-numpy.array(ray_origin)),_normal)/numpy.dot(ray_direction,_normal)
    #print(f't={t}')
    if t<0:
        return
    hit_position=ray_origin+t*ray_direction
    Barys=[]
    Bary_sums=0
    for i in range(3):
        v=getBarycentric_0f_edge(hit_position,tri_index,i)
        if v<-1e-10 :
            return
        Bary_sums=Bary_sums+v
        Barys.append(v)
    #print(f'{Barys}')
    #by commenting this out, i fixed spots on the triangle#if Bary_sums>1:
    #by commenting this out, i fixed spots on the triangle#    return
    rgb=numpy.array([0,0,0])
    #print(Bary_sums)
    for sun_index in range(len(sun_xs)):
        sun_position=numpy.array([sun_xs[sun_index],sun_ys[sun_index],sun_zs[sun_index]])
        light_direction=sun_position
        light_direction=light_direction/numpy.linalg.norm(light_direction)
        
        light_position_and_direction=[hit_position,light_direction]
        if collision_detection_only(light_position_and_direction,-1,tri_index):
            #print(f'sphere{sphere_index} is shadowed')
            continue
        #else:
            #print(f'sphere{sphere_index} not shadowed')
        normal_dot_view=numpy.dot(_normal,light_direction)
        if normal_dot_view<0:
            normal_dot_view=normal_dot_view*-1
        if tri_rgbs[tri_index][0]==-1:
            
            Barys
            _texcoords=[xyz_coords[tris[tri_index][i]] for i in range(3)]
            u=0.0
            v=0.0
            for i in range(3):
                u=u+Barys[i]*_texcoords[i][0] 
                v=v+Barys[i]*_texcoords[i][1] 
            texture=textures[tri_rgbs[tri_index][1]]
            texture_width, texture_height = texture.size
            #sprint(u,v)
            _r,_g,_b,_a=texture.getpixel((u%1*texture_width,v%1*texture_height))
            #print(_r)
            _rgb=[_r/255,_g/255,_b/255]
            _rgb=[srgb_to_linear(channel) for channel in _rgb]
        else:
            _rgb=tri_rgbs[tri_index]
            #_rgb=[ clamp(tosRGB(_rgb[i])) for i in range(3)]
        #print(_rgb)
        rgb=rgb+numpy.array([sun_rgbs[sun_index][0]*normal_dot_view*_rgb[0],
                            sun_rgbs[sun_index][1]*normal_dot_view*_rgb[1],
                            sun_rgbs[sun_index][2]*normal_dot_view*_rgb[2]])
        #rgb=rgb+numpy.array([normal_dot_view,normal_dot_view,normal_dot_view])
        #print(normal_dot_view)
    
    toAppend.append([tri_index,t,rgb])

def sphere_collision_detection(ray,sphere_index,toAppend):
    ray_origin,ray_direction=ray
    sphere_center=[sphere_xs[sphere_index],sphere_ys[sphere_index],sphere_zs[sphere_index]]
    sphere_r=sphere_rs[sphere_index]
    sphere_center=numpy.array(sphere_center)
    ray_origin=numpy.array(ray_origin)
    ray_direction=numpy.array(ray_direction)
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
    
    hit_position=ray_origin+ray_direction*d
    normal=hit_position-sphere_center
    normal=normal/numpy.linalg.norm(normal)
    rgb=numpy.array([0,0,0])
    if sphere_rgbs[sphere_index][0]==-1:
        longitude=(math.atan2(normal[0], normal[2])+math.pi*0.5)/(2*math.pi)
        lattitude=1-(math.atan2(normal[1],(normal[0]**2+normal[2]**2)**(1/2))+math.pi*0.5)/math.pi
        
        #longitude=(math.atan2(normal[0], normal[2]))/(2*math.pi)
        #lattitude=(math.atan2(normal[1],(normal[0]**2+normal[2]**2)**(1/2)))/math.pi
        texture=textures[sphere_rgbs[sphere_index][1]]
        texture_width, texture_height = texture.size
        _r,_g,_b,_a=texture.getpixel((longitude%1.0*texture_width,lattitude%1.0*texture_height))
        #print(_r)
        _rgb=[_r/255,_g/255,_b/255]
        _rgb=[srgb_to_linear(channel) for channel in _rgb]
    else:
        _rgb=sphere_rgbs[sphere_index]
    for sun_index in range(len(sun_xs)):
        sun_position=numpy.array([sun_xs[sun_index],sun_ys[sun_index],sun_zs[sun_index]])
        light_direction=sun_position
        light_direction=light_direction/numpy.linalg.norm(light_direction)
        
        light_position_and_direction=[hit_position,light_direction]
        shadowed=False
        if collision_detection_only(light_position_and_direction,sphere_index,-1):
            continue
        normal_dot_view=numpy.dot(normal,light_direction)
        
        rgb=rgb+numpy.array([sun_rgbs[sun_index][0]*normal_dot_view*_rgb[0],
                            sun_rgbs[sun_index][1]*normal_dot_view*_rgb[1],
                            sun_rgbs[sun_index][2]*normal_dot_view*_rgb[2]])
    for bulb_index in range(len(bulb_xyzs)):
        bulb_position=numpy.array(bulb_xyzs[bulb_index])
        light_direction=hit_position-bulb_position
        light_distance=numpy.linalg.norm(light_direction)
        light_direction=light_direction/light_distance
        
        light_position_and_direction=[hit_position,light_direction]
        shadowed=False
        if collision_detection_only(light_position_and_direction,sphere_index,-1):
            continue
        normal_dot_view=numpy.dot(normal,light_direction)
        
        bulb_light_intensity=(light_distance**2)**-1
        rgb=rgb+bulb_light_intensity*numpy.array([bulb_colors[bulb_index][0]*normal_dot_view*_rgb[0],
                            bulb_colors[bulb_index][1]*normal_dot_view*_rgb[1],
                            bulb_colors[bulb_index][2]*normal_dot_view*_rgb[2]])
        
    rgb=[clamp(i) for i in rgb]
                            
    
    toAppend.append([sphere_index,d,rgb])
    
    print(rgb[0]+rgb[1]+rgb[2])

if len(sys.argv) < 2:
    print("Usage: python your_program.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
#try:
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
        if newwords[0]=='texcoord':
            texcoord=[float(newwords[1]),float(newwords[2])]
            
        if newwords[0]=='texture':
            last_texture=newwords[1]
            if last_texture!='none':
                textures[newwords[1]]=Image.open(newwords[1])
            
            
            #texture_width, texture_height = texture.size
        if newwords[0]=='plane':
            plane_a=float(newwords[1])
            if plane_a==0:
                plane_a=0.000001
            plane_b=float(newwords[2])
            plane_c=float(newwords[3])
            plane_d=float(newwords[4])
            plane_normal=numpy.array([plane_a,plane_b,plane_c])
            plane_normal=plane_normal/numpy.linalg.norm(plane_normal)
            plane_point=numpy.array([-1*plane_d/plane_a,0,0])
            plane_normals.append(plane_normal)
            plane_points.append(plane_point)
            plane_rgbs.append(color)
        if newwords[0]=='xyz':
            xyz_s.append([float(newwords[1]),float(newwords[2]),float(newwords[3])])
            xyz_coords.append(texcoord)
            texcoord=[0,0]
        if newwords[0]=='tri':
            tri=[int(newwords[1]),int(newwords[2]),int(newwords[3])]
            tri=([i-1 if i>=0 else len(xyz_s)+i for i in tri])
            tris.append(tri)
            if last_texture=='none':
                tri_rgbs.append(color)
            else:
                tri_rgbs.append([-1,last_texture])
            _normal=numpy.cross(numpy.array(xyz_s[tri[1]])-numpy.array(xyz_s[tri[0]]),numpy.array(xyz_s[tri[2]])-numpy.array(xyz_s[tri[0]]))
            _normal=_normal/numpy.linalg.norm(_normal)
            tri_normals.append(_normal)
            tri_points.append(tri[0])
            #print(tri_points)
            edge_normals=[]
            for i in range(3):
                a=xyz_s[tri[i]]
                b=xyz_s[tri[(i+1)%3]]
                c=xyz_s[tri[(i+2)%3]]
                edge_normal=numpy.cross(numpy.array(c)-numpy.array(b),_normal)
                edge_normal=edge_normal/numpy.linalg.norm(edge_normal)
                edge2=numpy.array(a)-numpy.array(b)
                edge2_projected_on_edge_normal=getProject(edge2,edge_normal)
                edge_normals.append(edge2_projected_on_edge_normal)
            tris_edge_normals.append(edge_normals)
            #print(edge_normals)
        if newwords[0]=='png' :
            png_width=int(newwords[1])
            png_height=int(newwords[2])
            png_name=newwords[3]
        if newwords[0]=='color':
            color=[float(newwords[1]),float(newwords[2]),float(newwords[3])]
        if newwords[0]=='sphere' :
            sphere_x=float(newwords[1])
            sphere_y=float(newwords[2])
            sphere_z=float(newwords[3])
            sphere_r=float(newwords[4])
            sphere_xs.append(sphere_x)
            sphere_ys.append(sphere_y)
            sphere_zs.append(sphere_z)
            sphere_rs.append(sphere_r)
            if last_texture=='none':
                sphere_rgbs.append(color)
            else:
                sphere_rgbs.append([-1,last_texture])

            #print(sphere_z)
        if newwords[0]=='bulb':
            bulb_xyzs.append([float(newwords[1]),float(newwords[2]),float(newwords[3])])
            bulb_colors.append(color)
        if newwords[0]=='sun' :
            sun_x=float(newwords[1])
            sun_y=float(newwords[2])
            sun_z=float(newwords[3])
            sun_xs.append(sun_x)
            sun_ys.append(sun_y)
            sun_zs.append(sun_z)
            sun_rgbs.append(color)
    image = Image.new("RGBA", (png_width,png_height), (int(255*1/7),int(255*1/7),int(255*1/7),255))
    for x in range(png_width):
        for y in range(png_height):
            _x=(2*x-png_width)/max(png_width,png_height)
            _y=(2*y-png_height)*(-1)/max(png_width,png_height)
            ray_direction=[_x,_y,-1]
            ray_direction=ray_direction/numpy.linalg.norm(ray_direction)
            ray_origin=[0,0,0]
            ##v3 ray_direction=normalized(ray_direction)
            ##v3 d1=(sphere_center-ray_origin)
            ##v3 d2=ray_origin+tc*ray_direction-sphere_center
            ##v1 d3=sqrt(sphere_r**2-d2**2)
            collision_list=[]
            for sphere_index in range(len(sphere_xs)):
                ray=[ray_origin,ray_direction]
                sphere_collision_detection(ray,sphere_index,collision_list)
            for plane_index in range(len(plane_normals)):
                ray=[ray_origin,ray_direction]
                planes_collision_detection(ray,plane_index,collision_list)
            for tri_index in range(len(tri_normals)):
                ray=[ray_origin,ray_direction]
                tris_collision_detection(ray,tri_index,collision_list)
            
                #print(collision_list)
            
            if collision_list!=[]:
                nearest_hit=collision_list[0]
                for i in collision_list:
                    if i[1]<nearest_hit[1]:
                        nearest_hit=i
                
                rgb=[nearest_hit[2][0],nearest_hit[2][1],nearest_hit[2][2]]
                rgb = [clamp(tosRGB(channel)) for channel in rgb]
                image.im.putpixel((x,y),(int(rgb[0]*255),int(rgb[1]*255),int(rgb[2]*255),255))
            #larger than zero, least d1 sphere
            #
    #print([sun_xs[-1],sun_ys[-1],sun_zs[-1]])
    #print(tris)
    #print(xyz_s)
    image.save('bug.png')
#except BaseException: 
#    print(BaseException)
#finally:
#    print("ok")
                    