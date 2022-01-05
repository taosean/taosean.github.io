#function: 
#1, Get live_video from the webcam.
#2, With ROS publish Image_info (to yolo and so on).
#3, Convert directly, don't need to save pic at local.
 
import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
import sys
 
 
def webcamImagePub():
    # init ros_node
    rospy.init_node('rtsp_puber', anonymous=True)
    # queue_size should be small in order to make it 'real_time'
    # or the node will pub the past_frame
    img_pub = rospy.Publisher('rtsp/image_raw', Image, queue_size=2)
    rate = rospy.Rate(10) # 5hz
 
    # make a video_object and init the video object
    # stream = 'rtsp://admin:enflame123@192.168.100.248/h264/ch1/main/av_stream'
    #stream = 0
    stream = "/home/taoxuan/Projects/autoware.ai/calib_data/joint_calib_3.avi"
    cap = cv2.VideoCapture(stream)
    # define picture to_down' coefficient of ratio
    scaling_factor = 0.5
    # the 'CVBridge' is a python_class, must have a instance.
    # That means "cv2_to_imgmsg() must be called with CvBridge instance"
    bridge = CvBridge()
 
    if not cap.isOpened():
        sys.stdout.write("RTSP is not available !")
        return -1
 
    count = 0
    # loop until press 'esc' or 'q'
    while not rospy.is_shutdown():
        ret, frame = cap.read()

        # resize the frame
        if ret:
            count = count + 1
        else:
            rospy.loginfo("Capturing image failed. Retarting video capture")
            cap = cv2.VideoCapture(stream)

        if count == 1:
            count = 0
            frame = cv2.resize(frame,None,fx=scaling_factor,fy=scaling_factor,interpolation=cv2.INTER_AREA)
            msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            img_pub.publish(msg)
            print ('** publishing rtsp_frame ***')	
            
        rate.sleep()
 
if __name__ == '__main__':
    try:
        webcamImagePub()
    except rospy.ROSInterruptException:
        pass
