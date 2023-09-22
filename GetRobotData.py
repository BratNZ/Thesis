'''
The program will capture actual waypoint data

Regarding RTDE output:
   getActualTCPPose: this is RPY radians converted into RX, RY, RZ
   The joint angles were found to be more accurate after capturing all pose data
'''

import sys
import os
from datetime import datetime
import time
import math
from scipy.spatial.transform import Rotation

root = '~/' #specify the folder for image capture 

from rtde_control import RTDEControlInterface as RTDEControl
import rtde_receive

rtde_r = rtde_receive.RTDEReceiveInterface("192.168.1.100") #receive data from robot arm
#rtde_s = RTDEControl("192.168.1.100") #send data to robot arm

def main():
    timestamp=datetime.now().strftime("%y%m%d-%H%M%S")
    file_name="robot-" + timestamp + ".txt"
    file=open(file_name, 'w')
    file.close()
    start_time=time.time()
    initial_time=time.perf_counter()    
    while True:
        arm_time = str(int(rtde_r.getTimestamp() * 1000))
        pose = rtde_r.getActualTCPPose()
        place, angles = pose[:3], pose[3:] #translation and euler rotation of the robot
        tmp = Rotation.from_rotvec(angles)
        place = ",".join([str(x) for x in place])
        quat = ",".join([str(x) for x in tmp.as_quat()])
        line1 = arm_time + "," + place + "," + quat + "," + str(angles) + "\n"
        elapsed_time=time.perf_counter() - initial_time   
        print(str(elapsed_time),line1)
        with open(file_name, 'a') as file_handle:
            file_handle.write(line1)
        if elapsed_time >= 130:
            exit(0)

if __name__ == "__main__":
    main()

