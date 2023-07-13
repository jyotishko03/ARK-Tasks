import cv2
import numpy as np

collage1=cv2.imread("collage.png",0)
template1=cv2.imread("result.png",0)

def template_coord(template, collage):
    global prev_per
    template=template1.copy()
    collage=collage1.copy()

    min=np.inf
    min_coord=0
    for i in range(0,700):
        for j in range(0,700):
            sum=0
            trial_part=collage[i:i+100,j:j+100]
            pixel_sqdiff_matrix=(trial_part-template)**2 #matrix containng sq_diff of each coord of 2 images
            sum=np.sum(pixel_sqdiff_matrix)
            ''''if sum<min:
                min=sum
                min_coord=[i,j]'''
            if sum==0:
                min_coord = [i, j]
            if int((i+j/10)/8)>prev_per:
                prev_per=int((i+j/10)/8)
                print(f'Scanning: {prev_per} % completed')

    return min_coord
prev_per=0
pass_co_ord=template_coord(template1,collage1)
if pass_co_ord ==0:
    print('No match found')
else:
    password=int((pass_co_ord[0]+pass_co_ord[1])*3.1415926)
    print(f'co-ord matched: {pass_co_ord}')
    print(f'password: {password}')



