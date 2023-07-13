import cv2
import numpy as np
import random

maze=cv2.imread("maze_modified.png")
cv2.imshow('maze',maze)
cv2.waitKey(100)
map=maze.copy()

global max_dist
max_dist=15



BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [0, 0, 255]
GREEN = [0, 255, 0]
CYAN = [255, 255, 0]
BLUE = [255, 0, 0]
YELLOW = [0, 255, 255]


def calcDist(point, current):
    return ((point[0] - current[0]) ** 2 + (point[1] - current[1]) ** 2) ** (1 / 2)

def point_on_line_at_dist(p1,p2):
    Xn=0
    if p2[1] - p1[1] != 0:
        slope = ((p2[0] - p1[0]) / (p2[1] - p1[1]))
        if slope <= 1 and slope >= -1:
            if p2[1] - p1[1] > 0:
                f = 1
            else:
                f = -1
            for x in range(p1[1], p2[1]+f, f):
                y = int(((p2[0] - p1[0]) / (p2[1] - p1[1])) * (x - p1[1]) + p1[0])
                if (maze[y, x] == [0,0,0]).all():
                    return 0
                if calcDist([y,x],p1)>max_dist:
                    Xn=[y,x]
                    return Xn


        else:
            if p2[0] - p1[0] > 0:
                f = 1
            else:
                f = -1
            for y in range(p1[0], p2[0]+f, f):
                x = int(1 / ((p2[0] - p1[0]) / (p2[1] - p1[1])) * (y - p1[0]) + p1[1])
                if (maze[y, x] == [0,0,0]).all():
                    return 0
                if calcDist([y, x], p1) > max_dist:
                    Xn = [y, x]
                    return Xn

    elif p2[0] - p1[0] > 0:
        for y in range(p1[0], p2[0]+1):
            if (maze[y, p2[1]] == [0, 0, 0]).all():
                return 0
            if calcDist([y, p2[1]], p1) > max_dist:
                Xn = [y, p2[1]]
                return Xn

    elif p2[0] - p1[0] < 0:
        for y in range(p1[0], p2[0]-1, -1):
            if (maze[y, p2[1]] == [0, 0, 0]).all():
                return 0
            if calcDist([y, p2[1]], p1) > max_dist:
                Xn = [y, p2[1]]
                return Xn
    if calcDist(p2,p1)<=10:
        Xn=p2
    return Xn



def display_Path(map_path, start, end, node, parent):

    for i in range(len(node)):
        point=node[i]
        parent_point=parent[i]
        if point==start:
            cv2.circle(map_path, (start[1], start[0]), 4, RED, -1)
            continue
        map_path = cv2.line(map, (point[1],point[0]), (parent_point[1],parent_point[0]),[0,0,0], 1)
        cv2.circle(map_path, (point[1], point[0]), 3, BLUE, -1)
        cv2.imshow('map_path',map_path)
        cv2.imshow('maze', maze)
        cv2.circle(map_path, (end[1], end[0]), 30, GREEN, 2)
        cv2.circle(map_path, (start[1], start[0]), 4, RED, -1)

    cv2.waitKey(1)
def display_final_path(map_final_path,node,parent,Xn, start):
    while (Xn!=start):
        i=node.index(Xn)
        Xc=parent[i]
        map_final_path= cv2.line(map, (Xn[1],Xn[0]), (Xc[1],Xc[0]), [255,0,255], 2)
        cv2.imshow('map_final_path', map_final_path)
        Xn=Xc


def RRT(map, start, end):
    img = map.copy()
    h, w, t = img.shape
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    parent=[None]
    node=[start]

    iter=0
    while True:
        if iter>100000:
            print('iteration limit reached')
            break
        Xr=[random.randint(0,h-1), random.randint(0,w-1)]
        if (map[Xr[0],Xr[1]]!=WHITE).all():
            continue
        min_dist=np.inf
        for point in node:
            dist=calcDist(point,Xr)
            if dist<min_dist:
                min_dist=dist
                Xc=point


        if min_dist>max_dist:
            Xn=point_on_line_at_dist(Xc,Xr)
        else:
            #continue
            Xn=point_on_line_at_dist(Xc,Xr)

        if Xn == 0:
            continue



        node.append(Xn)
        parent.append(Xc)
        if calcDist(end,Xn)<30:
            print('Done')
            display_Path(img, start, end, node, parent)
            display_final_path(img, node, parent, Xn, start)
            cv2.waitKey(1000)
            break

        display_Path(map,start,end,node, parent)


        if cv2.waitKey(1)==ord('q'):
            break


start = (320,40)
end = (320,107)
RRT (map, start, end)

start = (48,164)
end = (307,432)
RRT (map, start, end)

#cv2.imwrite("maze_RRT_solved_6.png", map)
cv2.waitKey(0)

