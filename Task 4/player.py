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
imgMsg=np.full((512,512,3),0,np.uint8) #initial input
	
	
def strategy():
	global result
	result=None
	rospy.init_node('player_node')
	print("PLease wait while the image loads")
	print("It may take around 2 mins to get generated fully")
	print("and make the Successful Identification message visible")
	print("The transformation will slowly be visible in 'img' window meanwhile")
	rospy.Subscriber("/result", Image, guessCallback)
	

	while not rospy.is_shutdown():
					
		if result is None:
			result=np.full((512,512,3),1,np.uint8)
		lesser = np.where(result==0)
		more = np.where(result==255)
		imgMsg[lesser[0],lesser[1],(lesser[2]+1)%3] += 1 #changing image values by each time if not matched
		imgMsg[more[0],more[1],(more[2]+1)%3] -=1
		img_msg = bridge.cv2_to_imgmsg(imgMsg,"bgr8")
		cv2.imshow("img", imgMsg)
		cv2.imwrite(r"/home/jyotishko/catkin_ws/src/compute_image/scripts/image.png", imgMsg)
		cv2.waitKey(1)
		#cv2.destroyWindow("img")
		pub1.publish(img_msg)
		rospy.sleep(0.2)

def guessCallback(data):
	global result
	result = bridge.imgmsg_to_cv2(data,"bgr8")

	
	
if __name__ == '__main__':
	try:
		strategy()
			
	except rospy.ROSInterruptException:
		pass















