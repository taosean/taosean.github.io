from os import WIFSTOPPED
import numpy as np
import cv2

import yaml

from lidar_stream import LiDAR_Stream

if __name__ == '__main__':
    # get Nx4 point cloud data
    # lidar init
    pcap_file = "/home/taoxuan/Projects/autoware.ai/calib_data/person.pcap"
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

    calib_file = "/home/taoxuan/20210824_162528_autoware_lidar_camera_calibration.yaml"
    stream = "/home/taoxuan/Projects/autoware.ai/calib_data/person.avi"
    cap = cv2.VideoCapture(stream)

    ret, frame = cap.read()

    if ret:
        with open(calib_file, 'r') as f:
            params = f.read()
            params = yaml.load(params)

        cam_to_lidar_rows = params['CameraExtrinsicMat']['rows']
        cam_to_lidar_cols = params['CameraExtrinsicMat']['cols']
        cam_to_lidar_np = np.array(params['CameraExtrinsicMat']['data']).reshape(cam_to_lidar_rows, cam_to_lidar_cols)

        cam_intrinsic_rows = params['CameraMat']['rows']
        cam_intrinsic_cols = params['CameraMat']['cols']
        cam_intrinsic_np = np.array(params['CameraMat']['data']).reshape(cam_intrinsic_rows, cam_intrinsic_cols)

        distortion_coeff = np.array(params['DistCoeff']['data'])

        image_size = params['ImageSize']

        pc_data[:, -1] = 1
        points = np.transpose(pc_data)

        lidar_to_cam = np.linalg.inv(cam_to_lidar_np)

        points_on_cam_coord = np.matmul(lidar_to_cam, points)
        points_on_image = np.matmul(cam_intrinsic_np, points_on_cam_coord[:3, :])
        print('---')

        coords_on_images = points_on_image / points_on_image[2, :]

        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        img_hgt, img_wth = frame.shape[:2]
        
        cv2.namedWindow('Points to image', cv2.WINDOW_FREERATIO)

        frame_undistort = frame
        # Kprime, roi = cv2.getOptimalNewCameraMatrix(cam_intrinsic_np, distortion_coeff, (img_wth, img_hgt), 1, (img_wth, img_hgt))
        frame_undistort = cv2.undistort(frame, cam_intrinsic_np, distortion_coeff)#, None, Kprime)

        i = 0
        for point in np.transpose(coords_on_images[:2]):
            i += 1
            x, y = point

            if x < 0 or x >= img_wth or y < 0 or y >= img_hgt:
                continue

            cv2.circle(frame_undistort, (int(x), int(y)), 1, (0, 0, 255), -1)
            print('point ', i)

        cv2.imshow('Points to image', frame_undistort)
        cv2.waitKey(1000000)
