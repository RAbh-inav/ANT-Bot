#importing necessary libraries to the python file

#library for operating with the image
import cv2
#library to operate with pixel value matrix
import numpy as np
#library to display proceed image
import matplotlib.pyplot as plt

### start of Dijkstra algorithm

# class to assign parameters to be processed for each pixel value
class Vertex:
    def __init__(self,x_coord,y_coord):
        self.x=x_coord
        self.y=y_coord
        self.d=float('inf')
        self.parent_x=None
        self.parent_y=None
        self.processed=False
        self.index_in_queue=None

# function to get neighbour pixel values for a given pixel value
def get_neighbors(mat,r,c):
    shape=mat.shape
    neighbors=[]
    if r > 0 and not mat[r-1][c].processed:
         neighbors.append(mat[r-1][c])
    if r < shape[0] - 1 and not mat[r+1][c].processed:
            neighbors.append(mat[r+1][c])
    if c > 0 and not mat[r][c-1].processed:
        neighbors.append(mat[r][c-1])
    if c < shape[1] - 1 and not mat[r][c+1].processed:
            neighbors.append(mat[r][c+1])
    return neighbors

# populating the maze in the forward direction or upward direction and returning the corresponding values
def bubble_up(queue, index):
    if index <= 0:
        return queue
    p_index=(index-1)//2
    if queue[index].d < queue[p_index].d:
            queue[index], queue[p_index]=queue[p_index], queue[index]
            queue[index].index_in_queue=index
            queue[p_index].index_in_queue=p_index
            quque = bubble_up(queue, p_index)
    return queue
   
# populating the maze in the downwards direction or upward direction and returning the corresponding values
def bubble_down(queue, index):
    length=len(queue)
    lc_index=2*index+1
    rc_index=lc_index+1
    if lc_index >= length:
        return queue
    if lc_index < length and rc_index >= length:
        if queue[index].d > queue[lc_index].d:
            queue[index], queue[lc_index]=queue[lc_index], queue[index]
            queue[index].index_in_queue=index
            queue[lc_index].index_in_queue=lc_index
            queue = bubble_down(queue, lc_index)
    else:
        small = lc_index
        if queue[lc_index].d > queue[rc_index].d:
            small = rc_index
        if queue[small].d < queue[index].d:
            queue[index],queue[small]=queue[small],queue[index]
            queue[index].index_in_queue=index
            queue[small].index_in_queue=small
            queue = bubble_down(queue, small)
    return queue

#get pixel distance between two given point in the image
def get_distance(img,u,v):
    return 0.1 + (float(img[v][0])-float(img[u][0]))**2+(float(img[v][1])-float(img[u][1]))**2+(float(img[v][2])-float(img[u][2]))**2

#function to draw the resultant path on the input image
def drawPath(img,path, thickness=12):
    x0,y0=path[0]
    for vertex in path[1:]:
        x1,y1=vertex
        cv2.line(img,(x0,y0),(x1,y1),(255,0,0),thickness)
        x0,y0=vertex

#the main function to activate the above mentioned functions
def find_shortest_path(img,src,dst):
    pq=[]
    #src --> starting point of the input image
    #dst --> destination point of the input image

    source_x=src[0]
    source_y=src[1]
    dest_x=dst[0]
    dest_y=dst[1]
    imagerows,imagecols=img.shape[0],img.shape[1]
    matrix = np.full((imagerows, imagecols), None)
    #for loop to initialize the class vertex objects to the image
    for r in range(imagerows):
        for c in range(imagecols):
            matrix[r][c]=Vertex(c,r)
            matrix[r][c].index_in_queue=len(pq)
            pq.append(matrix[r][c])
    matrix[source_y][source_x].d=0
    pq=bubble_up(pq, matrix[source_y][source_x].index_in_queue)
    #while loop to populate the image
    while len(pq) > 0:
        u=pq[0]
        u.processed=True
        pq[0]=pq[-1]
        pq[0].index_in_queue=0
        pq.pop()
        pq=bubble_down(pq,0)
        neighbors = get_neighbors(matrix,u.y,u.x)
        for v in neighbors:
            dist=get_distance(img,(u.y,u.x),(v.y,v.x))
            if u.d + dist < v.d:
                v.d = u.d+dist
                v.parent_x=u.x
                v.parent_y=u.y
                idx=v.index_in_queue
                pq=bubble_down(pq,idx)
                pq=bubble_up(pq,idx)
                         
    path=[]
    iter_v=matrix[dest_y][dest_x]
    path.append((dest_x,dest_y))
    #while loop to find the shortest distance to reach the destination
    while(iter_v.y!=source_y or iter_v.x!=source_x):
        path.append((iter_v.x,iter_v.y))
        iter_v=matrix[iter_v.parent_y][iter_v.parent_x]

    path.append((source_x,source_y))
    return path

#input image
img = cv2.imread(r'C:\Users\Vaikunth Guruswamy\Downloads\ant-bot final\tarun.jpeg')
#cv2.imshow('oo',img)
img = cv2.resize(img,(700, 700))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
############## detect corners with the goodFeaturesToTrack function. #########
corners = cv2.goodFeaturesToTrack(gray, 27, 0.01, 10)
corners = np.int0(corners)
l=[]
for i in corners:
    #print(i.ravel())
    x, y = i.ravel()
    l.append([x,y])
    cv2.circle(img, (x, y), 5, 255, -1)

x_max=y_max=0
x_min=y_min=800
for index in l:
    if x_min>index[0]:
        x_min=index[0]
    if x_max<index[0]:
        x_max=index[0]
    if y_min>index[1]:
        y_min=index[1]
    if y_max<index[1]:
        y_max=index[1]
end_points=[[x_min,y_min],[x_min,y_max],[x_max,y_min],[x_max,y_max]]
#print(end_points)
######################################################################################
i = img[x_min:x_max,y_min:y_max]
cv2.imshow('original image',i)
img =i
p = find_shortest_path(img,(8,380),(496,654))
drawPath(img,p)
#print(p)
plt.figure(figsize=(7,7))
plt.imshow(img)
############################path extraction ###############

bg = np.ones(img.shape, dtype="uint8")
bg*=255

def drawPath(image,path, thickness=5):
    '''path is a list of (x,y) tuples'''
    x0,y0=path[0]
    for vertex in path[1:]:
        x1,y1=vertex
        cv2.line(image,(x0,y0),(x1,y1),(255,0,0),thickness)
        x0,y0=vertex

for i in range(len(p)-1):
    drawPath(bg, (p[i], p[i+1]))

cv2.imshow("result", bg)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite(r"C:\Users\Vaikunth Guruswamy\Downloads\ant-bot final\res.jpg", bg)
#############################edge detect ##################
 
 
# read the image
img = cv2.imread(r'C:\Users\Vaikunth Guruswamy\Downloads\maze solver\res.jpg')
img = cv2.resize(img,(700,700))
 
# convert image to grayscale image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
# detect corners with the goodFeaturesToTrack function.
corners = cv2.goodFeaturesToTrack(gray, 27, 0.01, 10)
corners = np.int0(corners)
l=[]
for i in corners:
    #print(i.ravel())
    x, y = i.ravel()
    l.append([x,y])
    cv2.circle(img, (x, y), 5, 0, -1)

x_max=y_max=0
x_min=y_min=800
# for loop to find the edgepoints of the given maze
for index in l:
    if x_min>index[0]:
        x_min=index[0]
    if x_max<index[0]:
        x_max=index[0]
    if y_min>index[1]:
        y_min=index[1]
    if y_max<index[1]:
        y_max=index[1]
end_points=[[x_min,y_min],[x_min,y_max],[x_max,y_min],[x_max,y_max]]
#print(end_points)
i = img[18:686,20:685]
 
plt.imshow(i)
o=p
ind =[]
import math
res={}
for i in l:
    for j in o:
        if((i[0] in range(j[0]-5,j[0]+5)) and (i[1] in range(j[1]-5,j[1]+5))):
            ind.append(j)
            res[o.index(j)] = j
            break


#print(res)
list_keys = list(res.keys())
list_keys.sort()
list_empty=[]
#print(list_keys)
for i in list_keys:
    list_empty.append(list(res[i]))
#print(list_empty)
#print(l)
l=list_empty
print('###################################final output##########################################')
################################inst
angle=0
import math
list_coordinates=l
difference=0
instruction=[]
y_len=float(input("enter the length of map along y:"))
x_len=float(input("enter the length of map along x:"))
#rpm=1000
x_ratio=x_len/700
y_ratio=y_len/700
for index in range(len(list_coordinates)-2,0,-1):
    y_diff=-(list_coordinates[index][1]-list_coordinates[index+1][1])*y_ratio
    x_diff=(list_coordinates[index][0]-list_coordinates[index+1][0])*x_ratio
    if x_diff!=0:
        slope=(math.atan(y_diff/x_diff)*180)/math.pi
    else:
        slope=90
    difference=angle-slope
    angle=slope
    distance=math.sqrt(y_diff**2+x_diff**2)
    if difference<0:
        instruction.append(["l",round(abs(difference)),distance])
    elif difference>0:
        instruction.append(["r", round(abs(difference)), distance])
    else:
        instruction.append(["s", round(abs(difference)), distance])

print('\nfinal instruction\n')
for i in instruction:
    print(i)
turning=[]
angles=[]
length=[]
for index in instruction:
    turning.append(index[0])
    angles.append(index[1])
    length.append(index[2])

for index in range(0,len(angles)):
    rev_index=len(list_coordinates)-1-index
    if angles[index]>90:
        angles.insert(index+1,90)
        turning.insert(index+1,turning[index])
        angles[index]=90
        length.insert(index+1,math.cos(length[index]))
        length[index]=math.sin(length[index])
print('\ndirection to be turned\n',turning)
print('\nangle to be turned\n',angles)
print('\ndistance to be covered after each instruction\n',length)

plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()
