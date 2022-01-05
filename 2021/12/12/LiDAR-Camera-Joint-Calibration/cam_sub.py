#function: 
#display the frame from another node.
 
import rospy
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
 
def callback(data):
    # define picture to_down' coefficient of ratio
    scaling_factor = 0.5
    global count,bridge
    count = count + 1
    if count == 1:
        count = 0
        cv_img = bridge.imgmsg_to_cv2(data, "bgr8")
        cv2.imshow("frame" , cv_img)
        cv2.waitKey(3)
    else:
        pass
 
def displayWebcam():
    rospy.init_node('rtsp_display', anonymous=True)
 
    # make a video_object and init the video object
    global count,bridge
    count = 0
    bridge = CvBridge()
    rospy.Subscriber('rtsp/image_raw', Image, callback)
    rospy.spin()
 
if __name__ == '__main__':
    displayWebcam()