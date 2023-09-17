#!/usr/bin/python

from __future__ import print_function
from datetime import datetime
import smbus
import time
import sys
import qwiic_tca9548a
import board
from adafruit_icm20x import GyroRange, AccelRange, MagDataRate, ICM20948

def I2C_setup(multiplexer,i2c_channel_setup):
  bus = smbus.SMBus(1)
  bus.write_byte(multiplexer,channel_bytearray[i2c_channel_setup])
#  time.sleep(0.01)
  #print("TCA9548A I2C channel status:", bin(bus.read_byte(multiplexer)))

multiplexor_address=0x70
channel_bytearray=[0b00000001,0b00000010,0b00000100,0b00001000,0b00010000,0b00100000,0b01000000,0b10000000]
enabled_channel_numberarray=[0,3,4,5,7]
enabled_channel_namearray=["RR","FR","CM","FL","RL"]

i2c=board.I2C()  # uses board.SCL and board.SDA

for channel in enabled_channel_numberarray:
    I2C_setup(multiplexor_address,channel)
    icm = ICM20948(i2c)
    icm.accelerometer_range = AccelRange.RANGE_2G
    icm.gyro_range = GyroRange.RANGE_250_DPS
    icm.magnetometer_data_rate = MagDataRate.RATE_100HZ
    icm.gyro_data_rate_divisor = 0
    # 125
    icm.accelerometer_data_rate_divisor = 0
    # 4095

# Correction values from calibration
#gyro_x_offset = [-0.02998955, -0.03219639,0.023254980,0.008131502,-0.00307724]
#gyro_y_offset = [0.01596670,0.00790274,0.00284742,-0.00708547,0.00518083]
#gyro_z_offset = [0.00715132,-0.00007248,-0.00007248,-0.00660733,0.00312161,-0.00114486]
#accel_x_scale = [0.10203479,0.10182106,0.10181778,0.10188015,0.10167629]
#accel_y_scale = [-0.10180081,0.10145538,0.10158317,0.10185943,0.10189014]
#accel_z_scale = [0.10115512,0.1009117,0.10140077,0.10123609,0.10135164]
#accel_x_offset = [0.00078995,-0.00159294,0.01240663,-0.00665329,0.0027521]
#accel_y_offset = [-0.01058559,0.01550039,0.0155684,-0.01244544,0.0128008]
#accel_z_offset = [-0.02925765,-0.01817877,-0.03045218,-0.01997862,0.00237755]
 
timestamp=datetime.now().strftime('%Y-%m-%d_%H%M')
filename= '' + timestamp + '.csv'
start_time=time.time()
print("Gathering IMU Data")
initialtime=time.perf_counter()
with open(filename,'a') as file_handle:
  while True:
    for channel in enabled_channel_numberarray:
      I2C_setup(multiplexor_address,channel)
      # icm = ICM20948(i2c)
      channel_index=enabled_channel_numberarray.index(channel)
      channel_name=enabled_channel_namearray[channel_index]
      elapsedtime=str(time.perf_counter() - initialtime)
      #acceleration=list(icm.acceleration)
      acceleration=','.join(map(str,icm.acceleration))
      #print("Raw Accel =",acceleration,"for IMU",channel)
      #acceleration[0] = acceleration[0]*accel_x_scale[channel_index]
      #acceleration[0] = acceleration[0]+accel_x_offset[channel_index]
      #acceleration[1] = acceleration[1]*accel_y_scale[channel_index]
      #acceleration[1] = acceleration[1]+accel_y_offset[channel_index]
      #acceleration[2] = acceleration[2]*accel_z_scale[channel_index]
      #acceleration[2] = acceleration[2]+accel_z_offset[channel_index]
      #accelerationstr=','.join(map(str,acceleration))
      #print("Calibrated Accel = ",accelerationstr)
      #gyro=list(icm.gyro)
      gyro=','.join(map(str,icm.gyro))
      #print(" Raw Gyro = ",gyro)
      #gyro[0] = gyro[0]+gyro_x_offset[channel_index]
      #gyro[1] = gyro[1]+gyro_y_offset[channel_index]
      #gyro[2] = gyro[2]+gyro_z_offset[channel_index]
      #gyrostr=','.join(map(str,gyro))
      #print(" Calibrated Gyro = ",gyrostr)
      op_line=','.join([channel_name,elapsedtime,acceleration,gyro]) 
      op_line+="\n"
      file_handle.write(op_line)
      #print(op_line)
      #print("Magnetometer X:%.2f, Y: %.2f, Z: %.2f uT" % (icm.magnetic))
      #time.sleep(0.1)
      elapsed_time=int(round((time.time() - start_time)))
      if elapsed_time >= 120:
        exit(0)
      print("Elapsed time is ", elapsed_time)

