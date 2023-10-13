%Kalman Filter using magnetometer
function [ kroll,kpitch,t ] = kalmanmagfilter(acc_x,acc_y,acc_z,gyr_x,gyr_y,gyr_z,mag_x,mag_y,mag_z)
	accel_data=[ acc_x acc_y acc_z ]
	gyro_data=[ gyr_x gyr_y gyr_z ]
    mag_data=[ mag_x mag_y mag_z ]
	FUSE=ahrsfilter(ReferenceFrame='NED',SampleRate=8.33,DecimationFactor=1,MagneticDisturbanceNoise=0.5,AccelerometerNoise=0.16,GyroscopeNoise=0.03,GyroscopeDriftNoise=3.04622e-2,LinearAccelerationNoise=0.0096236,LinearAccelerationDecayFactor=0.1,OrientationFormat='quaternion');
	start=tic;
	q=FUSE(accel_data,gyro_data,mag_data);
	kfilter=quat2eul(q,'ZYX');
	kroll=kfilter(:,3);
	kpitch=kfilter(:,2);
	t=toc(start)
end