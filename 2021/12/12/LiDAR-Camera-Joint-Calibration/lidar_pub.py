import numpy as np
import rospy

import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2
import std_msgs.msg

from lidar_stream import LiDAR_Stream


def publish_pc2(pc, obj):
    """Publisher of PointCloud data"""
    rospy.init_node("pc2_publisher")

    pub = rospy.Publisher("robosense/points_raw", PointCloud2, queue_size=1000000)
    header = std_msgs.msg.Header()
    header.stamp = rospy.Time.now()
    header.frame_id = "robosense"
    points = pc2.create_cloud_xyz32(header, pc[:, :3])
    #pub2 = rospy.Publisher("/points_raw1", PointCloud2, queue_size=1000000)
    #header = std_msgs.msg.Header()
    #header.stamp = rospy.Time.now()
    #header.frame_id = "velodyne"
    #points2 = pc2.create_cloud_xyz32(header, obj)

    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        pub.publish(points)
        #pub2.publish(points2)
        print ('** publishing point cloud frame ***')	

        r.sleep()


if __name__ == '__main__':
    # get Nx4 point cloud data
        # lidar init
    pcap_file = "/home/taoxuan/Projects/autoware.ai/calib_data/joint_calib_3.pcap"
    exec_file = '/home/taoxuan/Develop/rs_driver_getdata'
    shared_file = '/tmp/shm_lidar_robo'
    shm_stream = LiDAR_Stream(exec_file, shared_file, pcap_file)
    shm_read = shm_stream.create_shm()
    process = shm_stream.start_input_process()
    cnt = shm_stream.read_data_cnt(process)

    for _ in range(20):
        cnt = shm_stream.read_data_cnt(process)
        frame_lidar = shm_stream.read_shm(shm_read, cnt)
    cnt = shm_stream.read_data_cnt(process)
    frame_lidar = shm_stream.read_shm(shm_read, cnt)

    pc_data = np.copy(frame_lidar)

    # print(pc_data.shape)
    publish_pc2(pc_data, None)
