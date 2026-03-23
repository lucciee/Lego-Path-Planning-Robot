## Setup

1. Open VSCode and click File -> Open Folder -> ```cloned_location/lab4/controllers/main/```

    - In this folder you will find the main.py file. This is where you will write your code for this lab.

2. Open Webots and click File -> Open World -> ```cloned_location/lab4/worlds/lab4```

    - You should now see a scene that is setup for Lab 4 with some example obstacles. The robot begins .5 m to the right of bottom line. The robot should navigate around the obstacles (for the real evaluation, it may be between 2 and 6) reaching within 5 cm of a goal positioned at 2m x 2m. This should be completed within 3 minutes.
    - You will also see a line that goes from the start position to the goal. This can be used as reference for the Bug algorithms, for instance, a mideline if you want to implement Bug2.

## Bug Fixes

In the EV3Minstorm.proto, put all the bumper components and the ultrasonic components under their own single transform, that may be translated or rotated together.

## Lab 4

1. See the [Lab 4 Instructions](./lab4_instructions.pdf) for details on the lab.
2. For your reference, the webots sensors are mapped to the following ports:
- Left Wheel: Port.A
- Right Wheel: Port.B
- Left Bumper: Port.S1
- Gyroscope: Port.S2
- Ultrasonic: Port.S4
3. If you are using the gyroscope, you must call the update_gyro_angle() every iteration of the simulation for it to properly update. For example:

```
while self.robot.step(self.time_step) != -1:
    self.gyro_sensor.update_gyro_angle()
```

Make sure to comment it out when running on the real robot.

## Sensor Positioning

If you would like to move any sensors:

1. In the scene tree, right click on EV3Mindstorm "EV3Minstrom" -> Edit PROTO Source
2. Ultrasonic sensor: On lines 318-319, you may rotate or translate the ultrasonic sensor.
3. Bumper sensor: On lines 203-204, you may rotate or translate the bumper sensor.
4. Save the file
5. Reload the world by clicking File -> Reload World to see the changes, or Ctrl + Shift + R (Cmd + Shift + R on Mac)

### Running the code in Webots

Make sure the simulation is at time 0. If not, click the rewind button next to the scene time. Then press play to run your code. To use sound, unmute the volume on the tool bar.

### Running the code on the Lego Mindstorms EV3

1. For the code to work on the robot, comment out the following lines in main.py:

```
import sys
import random
import pathlib
import os
sys.path.append(str((pathlib.Path(os.getcwd())).parent)) # Add parent directory to sys.path
from pybricks.robot import RobotSingleton as _Robot
# Note: if you have matplotlib and want to visualize your robot's estimated pose in Webots (see extra credit), uncomment next line:
# from data_visualizer import DataVisualizer # Note: requires matplotlib to be installed! for example, if you have pip, in your terminal you can install via pip install matlpotlib
```

```
self.robot = _Robot().get_robot()
self.time_step = _Robot().get_time_step() 
```

2. In the run() function, replace the following line with ```while True:```:

```
while self.robot.step(self.time_step) != -1:
```

3. Plug your robot into your computer.
4. In the VSCode Explorer open the EV3DEV DEVICE BROWSER.
5. Click `Click here to connect to a device`.
6. Select your device from the list.
7. To run your code while viewing the terminal output, click Run -> Start Debugging or F5 or click Run -> Run Without Debugging or Ctrl + F5 (Cmd + F5 on Mac).
8. You may also upload the code to you robot and edit the directories on the robot via the EV3DEV DEVICE BROWSER.
9. See the [Tutorial](https://education.lego.com/v3/assets/blt293eea581807678a/bltb470b9ea6e38f8d4/5f8802fc4376310c19e33714/getting-started-with-micropython-v2_enus.pdf) for more directions.

## Editing the Webots world

1. Make sure the scene tree is visible. If it is not, click Tools -> Scene Tree or Ctrl + T (Cmd + T on Mac)

### Moving the floor markers and walls

1. Make sure your world is paused and at time 0
2. The floor markers and walls are now objects that can be moved and resized. To do so, click on the marker you would like edit. Then you may translate, rotate, or scale the object by changing the values within the scene tree. You may also drag them around the scene.
3. Save the file
4. Reload the world by clicking File -> Reload World to see the changes, or Ctrl + Shift + R (Cmd + Shift + R on Mac)

### Editing the Robot

1. In the scene tree, right click on EV3Mindstorm "EV3Minstrom" -> Edit PROTO Source
2. You may edit the robots appearance by copying and pasting different parts of the proto. Feel free to experiment with this on your own. However, this will not be supported by the TA or Instructor.
3. Save the file
4. Reload the world by clicking File -> Reload World to see the changes, or Ctrl + Shift + R (Cmd + Shift + R on Mac)
