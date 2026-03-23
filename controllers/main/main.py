#!/usr/bin/env pybricks-micropython

# ==========================Comment out when running on the real robot===================
import sys
import random
import pathlib
import os
sys.path.append(str((pathlib.Path(os.getcwd())).parent)) # Add parent directory to sys.path
from pybricks.robot import RobotSingleton as _Robot
# Note: if you have matplotlib and want to visualize your robot's estimated pose in Webots (see extra credit), uncomment next line:
# from data_visualizer import DataVisualizer # Note: requires matplotlib to be installed! for example, if you have pip, in your terminal you can install via pip install matlpotlib
# =======================================================================================

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.media.ev3dev import SoundFile, ImageFile

class MyController:
    def __init__(self):
        # =====================Comment out when running on the real robot========================
        self.robot = _Robot().get_robot()
        self.time_step = _Robot().get_time_step() 
        # =======================================================================================
    
        # Initialize robot, sensors, and motors
        self.ev3 = EV3Brick()

        # 2D Plot lists
        # self.position_list = []
        # self.theta_list = []
        # self.ultrasonic_sensor_list = []
        # self.counter = 0
       
    def actuate_motors(self, speed):
        # Helper function for running motors at a given speed
        pass

    def stop_motors(self):
        # Helper function for stopping motors
        pass

    def compute_position(self, left_angle, right_angle, delta_time):
        # Implement diffential drive kinematics to update the robot's position and orientation
        # Hint: Use the formula from the slides
        pass

    def run(self):
        #==================== Change to "while True:" when running on the real robot ============
        # while True:
        while self.robot.step(self.time_step) != -1:
        # If you are using the gyro sensor, you must call the update_gyro_angle() here for it to work
        # Example: self.gyro_sensor.update_gyro_angle()
        # Comment out when running on the real robot
        # =======================================================================================
           
           # Write main program here
           pass

def main():
    lab4 = MyController()
    lab4.run()

if __name__ == "__main__":
    main()