# Project Overview
This project implements **ROS 2** to allow a user to control multiple simulated autonomous vehicles through hand gestures with a **Tap-Strap 2** device. It listens to the tap topics and publishes commands to the vehicles based on the hand gestures. These commands are published through **Ackermann commands**. 

The https://github.com/TapWithUs/tap-python-sdk repository is integrated within this project in order to connect to the Tap-Strap device and publish the ROS 2 messages.

The **‎'src/ts_convoy_comm/ts_convoy_comm/ts_sub.py'** file maps binary values to a tap signal. These are the tap values are are within the file:
- 1: **Toggles on/off** (whether the commands are send to the vehicles or not)
- 2: **Pointer finger tap** (Drives forward at 1 m/s)
- 3: **Both thumb and index finger tap** (Gradual right turn at 1 m/s, 45° angle)
- 4: **Middle finger tap** (Speed up to 5 m/s, 60 m/s acceleration)
- 8: **Ring finger tap** (Gradual left turn at 1 m/s, -45° angle)

**The topics are only sent to the simulation if the toggle command has received an on input.**
