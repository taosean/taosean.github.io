import os, sys
import time
import subprocess
import numpy as np
import mmap
sys.path.append('..')
#from utils.log import Logger
#logger = Logger('debug').getlog()

class LiDAR_Stream():
    def __init__(self, exec_file, shared_file, pcap_file=None):
        self.exec_file = exec_file #lidar driver exec file
        self.shared_file = shared_file
        self.pcap_file = pcap_file
        self.data_num = 630 * 25 * 5 * 4
        self.data_size = self.data_num * 4

    def start_input_process(self):
        #logger.info('Starting Lidar input process pipe')
        # command = [self.exec_file, '-type', 'RSM1', '-shm', self.shared_file,  '-leaf_size', '0.035,0.035,0.05', '-cond_rem', '-3.2,3.2', '-trans_y', '6']    #'-1.7,1.6' '-msop', '9966', '-difop', '8877'  '-msop', '2020', '-difop', '2021'
        # command = [self.exec_file, '-type', 'RSM1', '-shm', self.shared_file,  '-leaf_size', '0.035,0.035,0.05', '-pitch', '0.02']    #'-1.7,1.6' '-msop', '9966', '-difop', '8877'  '-msop', '2020', '-difop', '2021'
        # command = [self.exec_file, '-type', 'RSM1', '-shm', self.shared_file, '-pitch', '0.175', '-z', '2.5']    #'-1.7,1.6' '-msop', '9966', '-difop', '8877'  '-msop', '2020', '-difop', '2021'
        # command = [self.exec_file, '-type', 'RSM1', '-shm', self.shared_file, '-msop', '9966']    #'-1.7,1.6' '-msop', '9966', '-difop', '8877'  '-msop', '2020', '-difop', '2021'
        command = [self.exec_file, '-type', 'RSM1', '-shm', self.shared_file, '-yaw', '-0.0', '-pitch', '1.1',]# used for calib
        # command = [self.exec_file, '-type', 'RSM1', '-shm', self.shared_file, '-yaw', '-0.0', '-pitch', '1.02',]# '-yaw', '-0.4']

        if self.pcap_file:
            extend_cmd = ['-pcap', self.pcap_file]
            command.extend(extend_cmd)
        
        # excute command
        #logger.info('command is {}'.format(command))
        return subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=10**8)
    
    def create_shm(self):
        if not os.path.isfile(self.shared_file):
            # create initial file
            with open(self.shared_file, "w+b") as fd:
                fd.seek(self.data_size - 1)
                fd.write(b'\x00')

        #size = os.path.getsize(self.shared_file)
        fd = os.open(self.shared_file, os.O_RDWR)
        mm = mmap.mmap(fd, self.data_size, access=mmap.ACCESS_READ) # size
        return mm

    def read_data_cnt(self, process):
        # this function to read the valid coordinate data number, 
        # it will be used for reading data from shm
        #logger.debug('Reading data cnt')
        in_bytes = process.stdout.readline()
        if len(in_bytes) == 0:
            cnt = None
        else:
            data = bytes.decode(in_bytes)
            #print (data)
            cnt = int(data)
            #logger.debug("there are {} node data".format(cnt//4))

        return cnt


    def read_shm(self, shm_read, cnt):
        #logger.debug('Reading shm')
        #t1 = time.time()
        shm_read.seek(0)
        size = cnt * 4 # float type 4 bytes
        buf = shm_read.read(size)
        frame = np.frombuffer(buf, dtype=np.float32).reshape([-1, 4])
        #t2 = time.time()
        #logger.debug("=====Reading Duration:{}".format(t2-t1))
        #logger.debug("frame shape:{}".format(frame.shape))
        #logger.debug(frame)
        #print ('!!', frame)
        return frame
    
    def shutdown_shm(self):
        self.shm_read.close()
    
    def get_stream_process(self):
        shm_read = self.create_shm()
        process = self.start_input_process()

        #while True:
        # for _ in range(3):    
        #     cnt = self.read_data_cnt(process)
        #     if cnt is None:
        #         #logger.info('LiDAR startm END')
        #         break

        cnt = self.read_data_cnt(process)
        frame = self.read_shm(shm_read, cnt)
        shm_read.close()

        return frame, cnt

#==============================================================================================
# TEST code
def shm_main():
    exec_file = '/home/pse/rs_drv/rs_driver_getdata'
    pcap_file = '/home/pse/rs_driver-1.3.0/samples/rsm1_test.pcap'
    shared_file = '/tmp/shm_lidar'
    shm_stream = LiDAR_Stream(exec_file, shared_file, pcap_file)
    shm_stream.get_stream_process()


if __name__ == '__main__':
    shm_main()
