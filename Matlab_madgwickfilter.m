% Create Madgwick Function to perform Madgwick Filter operations
function [ mroll, mpitch, t ] = madgwickfilter(datasize,acc_x,acc_y,acc_z,gyr_x,gyr_y,gyr_z,timedata)
	accel_data=[ acc_x acc_y acc_z ]
	gyro_data= [ gyr_x,gyr_y,gyr_z ]
	addpath('C:\Study\quaternion_library');
	AHRSOBJ=MadgwickAHRS('SamplePeriod', 1/100, 'Beta', 15.0);
	quaternion = zeros(length(timedata), 4);
	mfilter = zeros(length(timedata), 3);
	start=tic;
	for l = 1:10
		for t = 1:length(timedata)
			AHRSOBJ.UpdateIMU(gyro_data(t,:), accel_data(t,:));
			% gyroscope units must be radians
			% Output is in zyx order.
			quaternion(t, :) = AHRSOBJ.Quaternion;
			mfilter(t, :) = quat2eul(AHRSOBJ.Quaternion);
			mroll=mfilter(:,3);
			mpitch=mfilter(:,2);
		end
	end
	t=toc(start)
    t = t /10
end
