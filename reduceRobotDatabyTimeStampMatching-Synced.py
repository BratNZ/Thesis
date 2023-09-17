armfilename='d:/study/robot-230914-095937-roll'
imufilename='d:/study/2023-09-14_0959-roll.csv'
            
read_filename = armfilename + '.txt'
write_filename = armfilename + '-adjusted-synced.csv'
write_file_handle = open(write_filename, "w")
write_file_handle.write("")
write_file_handle.close()
arm_index = 0
# Obtained from manual inspection of data
arm_sync_offset=27170

# Grab File Data
with open(imufilename) as imu_data_handle:
    imudata=imu_data_handle.readlines()
with open(read_filename) as read_arm_handle:
    armdata=read_arm_handle.readlines()
    
eoimudata=len(imudata)
last_difference = 0
arm_index += arm_sync_offset

for imu_index in range (0,eoimudata):
    cameraname=imudata[imu_index][0:2]

    imu_minute_string=imudata[imu_index].split(",")[2]
    #print(imu_minute_string)
    imu_minute=imu_minute_string.split(":")[1]
    #print(imu_minute)
    imu_second=float(imu_minute_string.split(":")[2])
    #print(imu_second)
    
    entrynotfound = True
    while entrynotfound == True:
        if arm_index == (len(armdata)-1):
            entrynotfound=False
        arm_minute=armdata[arm_index].split(":")[1]
        approxarmsecond=armdata[arm_index].split(":")[2]
        arm_second=float(approxarmsecond.split(",")[0])
        difference = abs(arm_second - imu_second )
        next_index = arm_index + 1
        nextarmsecond=armdata[next_index].split(":")[2]
        next_arm_second=float(nextarmsecond.split(",")[0])
        next_difference = abs(next_arm_second - imu_second)
        last_index = arm_index - 1
        lastarmsecond=armdata[last_index].split(":")[2]
        last_arm_second=float(lastarmsecond.split(",")[0])
        last_difference = abs(last_arm_second - imu_second)
        #print(imu_index,imu_second,arm_index,last_arm_second,arm_second,next_arm_second,last_difference,difference,next_difference)
        # Theory is that we start where we left off last time and check if the difference of our current reading is less than the next reading.
        # If it is, we've found the best match.
        # We first work the easy case where the IMU and ARM minutes match.
        if imu_minute == arm_minute:
            if difference < next_difference:
                print("M=M:Found it at index", arm_index)
                entrynotfound = False
                date_time=str(armdata[2].split(",")[1])
                oplineTCP=str(armdata[arm_index].split(",")[3:6])
                oplineAngles=str(armdata[arm_index].split(",")[16:19])
                oplineEuler=str(armdata[arm_index].split(",")[12:15])
                oplineWristJoints=armdata[arm_index].split(",")[23:25]
                oplineWristJoints[0]=oplineWristJoints[0].replace('[','')
                oplineWristJoints[1]=oplineWristJoints[1].replace(']','')
                oplineWristJoints=str(oplineWristJoints)
                print(imu_index,imu_second,arm_index,last_arm_second,arm_second,next_arm_second,last_difference,difference,next_difference)
                line = ','.join([date_time,cameraname,oplineTCP,oplineAngles,oplineEuler,oplineWristJoints,"\n"])
                write_file_handle = open(write_filename, "a")
                write_file_handle.write(line)
                write_file_handle.close()
                arm_index += 1
                break
            if difference > last_difference and next_difference > difference:
                # We've missed it - carry on
                arm_index += 1
                break
        # When IMU minutes and ARM minutes do not match, the best match might be our last one.
        if imu_minute != arm_minute:
            if last_difference < difference:
                print('M!=M:Found it at last index', last_index)
                entrynotfound = False
                oplineTCP=str(armdata[last_index].split(",")[3:6])
                oplineAngles=str(armdata[last_index].split(",")[16:19])
                oplineEuler=str(armdata[arm_index].split(",")[12:15])
                oplineWristJoints=armdata[last_index].split(",")[23:25]
                oplineWristJoints[0]=oplineWristJoints[0].replace('[','')
                oplineWristJoints[1]=oplineWristJoints[1].replace(']','')
                oplineWristJoints=str(oplineWristJoints)
                print(imu_index,imu_second,arm_index,last_arm_second,arm_second,next_arm_second,last_difference,difference,next_difference)
                line = ','.join([date_time,cameraname,oplineTCP,oplineAngles,oplineEuler,oplineWristJoints,"\n"])
                write_file_handle = open(write_filename, "a")
                write_file_handle.write(line)
                write_file_handle.close()
                arm_index += 1
                break
            if difference < next_difference:
                print('M!=M:Found it at current index', arm_index)
                entrynotfound = False
                oplineTCP=str(armdata[arm_index].split(",")[3:6])
                oplineAngles=str(armdata[arm_index].split(",")[16:19])
                oplineEuler=str(armdata[arm_index].split(",")[12:15])
                oplineWristJoints=armdata[arm_index].split(",")[23:25]
                oplineWristJoints[0]=oplineWristJoints[0].replace('[','')
                oplineWristJoints[1]=oplineWristJoints[1].replace(']','')
                oplineWristJoints=str(oplineWristJoints)
                print(imu_index,imu_second,arm_index,last_arm_second,arm_second,next_arm_second,last_difference,difference,next_difference)
                line = ','.join([date_time,cameraname,oplineTCP,oplineAngles,oplineEuler,oplineWristJoints,"\n"])
                write_file_handle = open(write_filename, "a")
                write_file_handle.write(line)
                write_file_handle.close()
                arm_index += 1
                break        
        arm_index += 1
print('Finished')    
