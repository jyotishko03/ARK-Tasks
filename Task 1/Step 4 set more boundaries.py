import cv2
import numpy as np
import keyboard

map=cv2.imread(r"maze.png")
map2=map.copy()
color = np.zeros((300, 512, 3), np.uint8)
map= cv2.line(map, [12,326], [70,326], [0,0,0], 5)
map= cv2.line(map, [133,34], [190,34], [0,0,0], 5)
#cv2.imwrite("maze_modified.png", map)
cv2.imshow('maze_original', map2)
cv2.imshow('maze_modified', map)
cv2.waitKey(0)