import numpy
# Online Python - IDE, Editor, Compiler, Interpreter
#a=[0.5,0.5,1,1,0,0,0]
#b=[0.5,-0.5,1,1,255,0,0]
#c=[0.5,-0.5,-1,0,255,0,0]
#points=[a,b,c]
#def append_points_by_append_xs_ys_zs(point):
#        x.append(point[0])
#        y.append(point[1])
#        z.append(point[2])
#        w.append(point[3])
#        r.append(point[4])
#        g.append(point[5])
#        b.append(point[6])

#x=[]
#y=[]
#z=[]
#w=[]
#r=[]
#g=[]
#b=[]
#for point in points:
#    append_points_by_append_xs_ys_zs(point)
#plane=numpy.array([-1,0,0,1])
#tris=[[0,1,2]]
def clip_and_append_xsyszs_and_tris(plane,tri_index,tris,x,y,z,w,r,g,b):
    reference_data=[
        [[2,0],[0,1],[1,2,3,4]],#if the inside or outside point is tri[0],the intersection point a is constructed using tri[2] and tri[0],
                                #and intersection point b is constructed using tri[0] and tri[1],and the first new triangle is of indexs:[tri[1],tri[2],tri[3]], and if its the outside point, then the second tri:[[tri[3],tri[4],tri[0]]
        [[0,1],[1,2],[0,3,4,2]],#if the inside or outside point is tri[1]
        [[1,2],[2,0],[0,1,3,4]]#if the inside or outside point is tri[2]
        ]
    
    def append_points_by_append_xs_ys_zs(point):
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
        w.append(point[3])
        r.append(point[4])
        g.append(point[5])
        b.append(point[6])
    def get_interception_point_by_index(index_1,index_2,mat_mult_results):
        
            if (mat_mult_results[index_1]-mat_mult_results[index_2])==0:
                print(f'''zero!xyzw=({x[tris[tri_index][index_1]],y[tris[tri_index][index_1]],z[tris[tri_index][index_1]],w[tris[tri_index][index_1]]})
                ({x[tris[tri_index][index_2]],y[tris[tri_index][index_2]],z[tris[tri_index][index_2]],w[tris[tri_index][index_2]]})
                lerpratio={mat_mult_results[index_1]}/{mat_mult_results[index_1]}-{mat_mult_results[index_2]}''')
            
            lerpratio=mat_mult_results[index_1]/(mat_mult_results[index_1]-mat_mult_results[index_2])
        
            toreturn=[]
            toreturn.append(lerp(x[tris[tri_index][index_1]],x[tris[tri_index][index_2]],lerpratio))
            toreturn.append(lerp(y[tris[tri_index][index_1]],y[tris[tri_index][index_2]],lerpratio))
            toreturn.append(lerp(z[tris[tri_index][index_1]],z[tris[tri_index][index_2]],lerpratio))
            toreturn.append(lerp(w[tris[tri_index][index_1]],w[tris[tri_index][index_2]],lerpratio))
            toreturn.append(lerp(r[tris[tri_index][index_1]],r[tris[tri_index][index_2]],lerpratio))
            toreturn.append(lerp(g[tris[tri_index][index_1]],g[tris[tri_index][index_2]],lerpratio))
            toreturn.append(lerp(b[tris[tri_index][index_1]],b[tris[tri_index][index_2]],lerpratio))
            return toreturn
    def lerp(a,b,ratio):
        return (b-a)*ratio+a
    #print(f'aaaa{[w[tris[tri_index][i]] for i in range(3)]}')
    points_in_this_tri=[numpy.array([x[tris[tri_index][i]],y[tris[tri_index][i]],z[tris[tri_index][i]],w[tris[tri_index][i]]]) for i in range(3)]
    
    mat_mult_results=[numpy.matmul(plane,i) for i in points_in_this_tri]
   #print(mat_mult_results)

    number_of_inside_points=0
    for i in mat_mult_results:
        if(i>=0):
            number_of_inside_points+=1
   #print(number_of_inside_points)
    if(number_of_inside_points==3):#if all are inside, do nothing
        return
    if(number_of_inside_points==0):#if all are outside, set this tri[0] to -1, so it does not get rendered
        tris[tri_index][0]=-1
        tris[tri_index][1]=-1
        tris[tri_index][2]=-1
        return
    if(number_of_inside_points==1):#if only one point is inside, cut to and append one tri 
        inside_point_index=0
        for i in range(len(mat_mult_results)):
           #print(f"aaa{tris[tri_index][i]}")
            if mat_mult_results[i]>=0:
                inside_point_index=i
        #print(f'bbb{inside_point_index}')
        reference_data[inside_point_index][0][0]
        points_to_construct_new_tris=[]
        points_to_construct_new_tris.append(tris[tri_index][0])
        points_to_construct_new_tris.append(tris[tri_index][1])
        points_to_construct_new_tris.append(tris[tri_index][2])
        
        point_1_index=len(x)
        points_to_construct_new_tris.append(point_1_index)
        point_1=get_interception_point_by_index(reference_data[inside_point_index][0][0],reference_data[inside_point_index][0][1],mat_mult_results)
        append_points_by_append_xs_ys_zs(point_1)
        
        point_2_index=len(x)
        points_to_construct_new_tris.append(point_2_index)
        point_2=get_interception_point_by_index(reference_data[inside_point_index][1][0],reference_data[inside_point_index][1][1],mat_mult_results)
        append_points_by_append_xs_ys_zs(point_2)
        
        tris.append([tris[tri_index][inside_point_index],points_to_construct_new_tris[3],points_to_construct_new_tris[4]])
        tris[tri_index][0]=-1
        
    if(number_of_inside_points==2):# if only two points are inside, cut to and append two tris
        outside_point_index=0
        for i in range(1,3):
            if mat_mult_results[i]<0:
                outside_point_index=i
        
       #print(outside_point_index)
        reference_data[outside_point_index][0][0]
        points_to_construct_new_tris=[]
        points_to_construct_new_tris.append(tris[tri_index][0])
        points_to_construct_new_tris.append(tris[tri_index][1])
        points_to_construct_new_tris.append(tris[tri_index][2])
        
        point_1_index=len(x)
        points_to_construct_new_tris.append(point_1_index)
        point_1=get_interception_point_by_index(reference_data[outside_point_index][0][0],reference_data[outside_point_index][0][1],mat_mult_results)
        append_points_by_append_xs_ys_zs(point_1)
        
        point_2_index=len(x)
        points_to_construct_new_tris.append(point_2_index)
        point_2=get_interception_point_by_index(reference_data[outside_point_index][1][0],reference_data[outside_point_index][1][1],mat_mult_results)
        append_points_by_append_xs_ys_zs(point_2)
        
        tris.append([points_to_construct_new_tris[reference_data[outside_point_index][2][0]],points_to_construct_new_tris[reference_data[outside_point_index][2][1]],points_to_construct_new_tris[reference_data[outside_point_index][2][2]]])
        tris.append([points_to_construct_new_tris[reference_data[outside_point_index][2][2]],points_to_construct_new_tris[reference_data[outside_point_index][2][3]],points_to_construct_new_tris[reference_data[outside_point_index][2][0]]])
        tris[tri_index][0]=-1
    
#clip_and_append_xsyszs_and_tris(plane,0,tris,x,y,z,w,r,g,b)
#print(x)
#print(mat_mult_results)
#print(lerp(0,-2,0.5))

#print(x)
#print(y)
#print(z)
#print(w)
#print(r)
#print(g)
#print(b)
#
#print(tris)
#print(mat_mult_results)
#print(lerp(0,-2,0.5))
#if frustum:
#        planes=[numpy.array([1,0,0,1]),
#        numpy.array([-1,0,0,1]),
#        numpy.array([0,1,0,1]),
#        numpy.array([0,-1,0,1]),
#        numpy.array([0,0,1,1]),
#        numpy.array([0,0,-1,1]),]
#        for plane in planes:
#            for i in range(len(tris)):
#                if tris[i][0]==-1:
#                    continue
#                clip_and_append_xsyszs_and_tris(plane,i,tris,x,y,z,w,r,g,b)