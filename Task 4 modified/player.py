#!/usr/bin/env python3
import rospy
import std_msgs
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np


pub1 = rospy.Publisher('/guess', Image, queue_size=10)
bridge = CvBridge()

global imgMsg
imgMsg=np.full((512,512,3),127,np.uint8) #initial input
	
	
def strategy():
	global result
	result=None
	rospy.init_node('player_node')
	print("PLease wait while the image loads")
	rospy.Subscriber("/result", Image, guessCallback)
	
	#The following 2 describes the upper limit and lower limit
	arr_low=np.full((512,512,3), 0)
	arr_high=np.full((512,512,3), 255)

	

	while not rospy.is_shutdown():
		global imgMsg
		#gets the co-ordinate where 0 and 255 are present
		lesser = np.where(result==0)
		more = np.where(result==255)
		perfect=np.where(result==127)
		if result is None:
			result=np.full((512,512,3),1,np.uint8)

		'''for i in range(512):
			for j in range(512):
				for k in range(3):

					if result[i][j][k]==127:
						continue

					elif result[i][j][k]==0:
						arr_low[i][j][(k+1)%3]=(arr_low[i][j][(k+1)%3]+arr_high[i][j][(k+1)%3])//2

					elif result[i][j][k]==255:
						arr_high[i][j][(k+1)%3]=(arr_low[i][j][(k+1)%3]+arr_high[i][j][(k+1)%3])//2'''
		
		try:
			arr_low[lesser[0],lesser[1],(lesser[2]+1)%3]=(arr_low[lesser[0],lesser[1],(lesser[2]+1)%3]+arr_high[lesser[0],lesser[1],(lesser[2]+1)%3])//2
			arr_high[more[0],more[1],(more[2]+1)%3]=(arr_low[more[0],more[1],(more[2]+1)%3]+arr_high[more[0],more[1],(more[2]+1)%3])//2
		
			#arr_mid=(arr_low+arr_high)//2
		
			imgMsg[lesser[0],lesser[1],(lesser[2]+1)%3]=(arr_low[lesser[0],lesser[1],(lesser[2]+1)%3]+arr_high[lesser[0],lesser[1],(lesser[2]+1)%3])//2
			imgMsg[more[0],more[1],(more[2]+1)%3]=(arr_low[more[0],more[1],(more[2]+1)%3]+arr_high[more[0],more[1],(more[2]+1)%3])//2
		
		except:
			pass

		img_msg = bridge.cv2_to_imgmsg(imgMsg,"bgr8")
		cv2.imshow("img", imgMsg)
		#cv2.imwrite(r"/home/jyotishko/catkin_ws/src/compute_image/scripts/image.png", imgMsg)
		cv2.waitKey(1)
		#cv2.destroyWindow("img")
		pub1.publish(img_msg)
		rospy.sleep(0.3)
'''def binary_search(arr, low, high, x):
 
    # Check base case
    if high >= low:
 
        mid = (high + low) // 2
 
        # If element is present at the middle itself
        if arr[mid] == x:
            return mid
 
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)
 
        # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)
 
    else:
        # Element is not present in the array
        return -1
    


def binary_search(arr,res):
    
    mid=(arr[0]+arr[1])//2
    
    if arr[mid] == x:
        return mid
 
        # If element is smaller than mid, then it can only
        # be present in left subarray
    elif arr[mid] > x:
        return binary_search(arr, low, mid - 1, x)
 
        # Else the element can only be present in right subarray
    else:
        return binary_search(arr, mid + 1, high, x)
 '''

def guessCallback(data):
	global result
	result = bridge.imgmsg_to_cv2(data,"bgr8")

	
	
if __name__ == '__main__':
	try:
		strategy()
			
	except rospy.ROSInterruptException:
		pass















