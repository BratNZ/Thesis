# Thesis
Thesis Repo

This github repository is for code relating to my Masters of Applied Computing thesis on using IMUs to adjust for bouncing of a vehicle under motion.
The thesis examines Madgwick, Kalman and Neural network approaches

To use this code:

1. Start robot arm data collection with Script_GetRobtoData.py (this was run under a Ubuntu LinuxforWindows container)
2. Grab some appropriate imu data using Script_imudata.py
3. Copy gathered data to a Matlab folder.
4. Run the commands in Matlab_commands-Varied.txt to process the Madgwick and Kalman filters over the data.
5. Align robot arm data and imu data manually by visual inspection of datasets.
6. Edit Matlab command file with settings foudn in step 5.
7 Analyse results.
8. Run nnstart and select a "fitting" model and import the appropriate training arrays.
9. Train nn and make changes to layers/models until a good fit is found.
10. Run Matlab-live script to process live data that has not been seen by the nn to test if model works for unfamiliar data.

 
