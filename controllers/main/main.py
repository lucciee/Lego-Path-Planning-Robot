#!/usr/bin/env pybricks-micropython

# ==========================Comment out when running on the real robot===================
# import sys
# import random
# import pathlib
# import os
# sys.path.append(str((pathlib.Path(os.getcwd())).parent)) # Add parent directory to sys.path
# from pybricks.robot import RobotSingleton as _Robot
# Note: if you have matplotlib and want to visualize your robot's estimated pose in Webots (see extra credit), uncomment next line:
# from data_visualizer import DataVisualizer # Note: requires matplotlib to be installed! for example, if you have pip, in your terminal you can install via pip install matplotlib
# =======================================================================================
import math
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.media.ev3dev import SoundFile, ImageFile


class MyController:
    def __init__(self):
        # =====================Comment out when running on the real robot========================
        # self.robot = _Robot().get_robot()
        # self.time_step = _Robot().get_time_step() 
        # =======================================================================================
    
        # Initialize robot, sensors, and motors
        self.ev3 = EV3Brick()
        self.left_motor = Motor(Port.A)
        self.right_motor = Motor(Port.B)
        self.left_bumper = TouchSensor(Port.S1)
        self.right_bumper = TouchSensor(Port.S3)
        self.gyroscope = GyroSensor(Port.S2)
        self.ultrasonic = UltrasonicSensor(Port.S4)

        # Parameters
        self.speed = 360    # degrees/sec

        # ===== Real robot measurements=======
        self.r = 0.0275         # wheel radius
        self.L = 0.1195         # distance between wheels
        
        # Position
        self.left_angle = 0
        self.right_angle = 0
        self.x = 0.5      # meters
        self.y = 0      # meters
        self.theta = math.pi/2  # radians, ccw is positve, x axis = 0, y axis = pi/2

        
        self.goal_x, self.goal_y = 3.0, 3.0 # 3 meters
        self.goal_radius = 0.05 # 5 cm
        self.goal_dist = math.sqrt(15.25)
        self.d_goal_dist = 0

        self.hit_point_goal_dist = math.sqrt(15.25)
        
        self.prev_error = 0
        self.ideal_wall_dist = 180   # mm

        self.goal_count = 0

        # reverse distance tracking
        self.reverse_start_x = 0
        self.reverse_start_y = 0

        # keep last good ultrasonic reading
        self.last_valid_ultra = 180


    def run_tank(self, left_speed, right_speed = None):
        if (right_speed == None):
            right_speed = left_speed
        self.left_motor.run(left_speed)
        self.right_motor.run(right_speed)

    def stop_motors(self):
        # Helper function for stopping motors
        self.left_motor.hold()
        self.right_motor.hold()
        wait(1000)

    def compute_position(self):
        left_angle = self.left_motor.angle()
        right_angle = self.right_motor.angle()
        gyro_angle = self.gyroscope.angle()

        # 1. Current distance traveled per wheel
        d_left = self.r * math.radians(left_angle - self.left_angle)
        d_right = self.r * math.radians(right_angle - self.right_angle)
        
        # 2. Calculate THEORETICAL angle change from wheels
        # (Right - Left) / TrackWidth
        delta_theta_wheels = (d_right - d_left) / self.L
        
        # 3. Calculate ACTUAL angle change from Gyro
        new_theta = math.radians(-gyro_angle)
        delta_theta_gyro = new_theta - self.theta
        
        # 4. Check for discrepancy (Threshold of ~0.05 rad or ~3 degrees)
        # If wheels say we turned but gyro says we didn't, we are slipping/stuck
        if abs(delta_theta_wheels - delta_theta_gyro) < 0.05:
            # NO DISCREPANCY: Update position normally
            d_center = (d_left + d_right) / 2.0
            self.x += d_center * math.cos((self.theta + new_theta) / 2.0)
            self.y += d_center * math.sin((self.theta + new_theta) / 2.0)
        else:
            self.ev3.speaker.beep(frequency=800, duration=200)
            
        # Update state for next iteration
        self.theta = new_theta
        self.left_angle = left_angle
        self.right_angle = right_angle


        new_goal_dist = self.compute_goal_dist()
        self.d_goal_dist = new_goal_dist - self.goal_dist
        self.goal_dist = new_goal_dist


    def compute_goal_dist(self):
        return math.sqrt((3 - self.x)**2 + (3- self.y)**2)

    def correct_drift(self, correction):
        # positive correction -> turn counterclockwise
        self.right_motor.run(self.speed + correction)
        self.left_motor.run(self.speed - correction)


    def rotate(self, degrees): #clockwise rotation if degrees is positive
        total_dist = math.pi * self.L * (degrees / 360)
        total_motor_degrees = math.degrees(total_dist / self.r)
        
        self.left_motor.run_angle(150, total_motor_degrees, wait=False)
        self.right_motor.run_angle(150, -total_motor_degrees, wait=True)

    def rotate_to_goal(self):
        target_theta = math.degrees(math.atan2(self.goal_y - self.y, self.goal_x - self.x))
        error = (target_theta - (-self.gyroscope.angle())) % 360
        if error > 180:
            error -= 360
        self.rotate(-error)

    def reverse(self):
        self.right_angle = self.right_motor.angle()
        self.left_angle = self.left_motor.angle()
        self.reverse_start_x = self.x
        self.reverse_start_y = self.y
        self.run_tank(-1 * self.speed)


    def get_filtered_ultra(self):
        vals = []
        for _ in range(10):
            d = self.ultrasonic.distance()
            if 60 <= d <= 700:
                vals.append(d)
            # wait(10)

        if len(vals) == 0:
            return None

        avg = sum(vals) / len(vals)
        self.last_valid_ultra = avg
        return avg
    

    def residual(self):
        def f(x): # m-line function
            return 1.2 * x - 0.6
        return abs(self.y - f(self.x))

    def run(self):
        self.gyroscope.reset_angle(-90)
        print("x_pos,y_pos")

        #==================== Change to "while True:" when running on the real robot ============
        while True: 
            pressed_buttons = self.ev3.buttons.pressed()

            if Button.CENTER in pressed_buttons:
                self.ev3.speaker.beep(frequency=500, duration=100)
                break

        while True:
        # while self.robot.step(self.time_step) != -1:
        # =======================================================================================
           
            # update positioning
            self.compute_position()
            # print("x" + str(self.x) + "  y" + str(self.y))
            # print(self.goal_dist)
            print("{},{}".format(self.x, self.y))

            if(self.goal_dist < 0.05):  # stop if within 5 cm of goal
                self.stop_motors()
                print(self.goal_dist)
                self.ev3.speaker.beep(frequency=800, duration=400)
                break


            if (self.goal_count == 0):
                self.rotate_to_goal()
                self.speed = 360
                self.run_tank(self.speed)
                self.goal_count += 1
                continue

            # execute goal 1: hit wall and reverse
            elif (self.goal_count == 1 and (self.left_bumper.pressed() or self.right_bumper.pressed())):
                self.stop_motors()
                self.reverse()
                self.goal_count += 1
            elif(self.goal_count == 1 and self.d_goal_dist > 0): # if distance from goal is increasing, stop and rotate to goal
                self.goal_count = 0
                self.d_goal_dist = 0

            # execute goal 2: stop reversing and rotate 90 degrees
            elif (self.goal_count == 2 and math.sqrt((self.x - self.reverse_start_x)**2 + (self.y - self.reverse_start_y)**2) >= 0.15):
                self.stop_motors()
                self.rotate(90)
                self.goal_count += 1
    
            # execute goal 3: record hit point
            elif (self.goal_count == 3):        # and self.theta >= math.pi / 2):
                # fixed target works better than trusting one noisy reading
                self.ideal_wall_dist = self.get_filtered_ultra()  # 180
                if (self.ideal_wall_dist == None):
                    self.ideal_wall_dist = 180

                self.hit_point_goal_dist = self.compute_goal_dist()

                self.speed = 250
                self.goal_count += 1
                self.run_tank(self.speed)

            # wall-follow object
            elif (self.goal_count == 4):
                if (self.residual() < 0.025 and self.goal_dist < (self.hit_point_goal_dist - 0.05)): # if within 5 cm of m-line
                    self.goal_count = 0
                    continue

                #if robot runs into wall
                if (self.right_bumper.pressed()): 
                    self.stop_motors()
                    self.reverse()
                    self.goal_count = -2
                    continue
                if (self.left_bumper.pressed()):
                    self.stop_motors()
                    self.reverse()
                    self.goal_count = -1
                    continue
                
                current_dist = self.get_filtered_ultra()

                # bad reading / lost wall
                if current_dist is None:
                    # gently turn left to reacquire wall
                    self.run_tank((self.speed* 0.8)/1.3, (self.speed *1.4 )/1.3)
                    # print("lost wall")
                    # wait(20)
                    continue

                error = current_dist - self.ideal_wall_dist

                # stronger correction when too close, softer when too far
                if current_dist < 120:
                    self.run_tank(self.speed * 1.56, self.speed * 0.56)
                    # print("hard right")
                elif current_dist < 155:
                    self.run_tank(self.speed *1.3 , self.speed * 0.8)
                    # print("right")
                elif current_dist > 260:
                    self.run_tank(self.speed *0.8 , self.speed * 1.4)
                    # print("hard left")
                elif current_dist > 220:
                    self.run_tank(self.speed * 0.9, self.speed *1.25)
                    # print("left")
                else:
                    self.run_tank(self.speed)
                    # print("straight")

                self.prev_error = error

            # goal_count = -1 or -2 when robot runs into wall
            if (self.goal_count < 0 and math.sqrt((self.x - self.reverse_start_x)**2 + (self.y - self.reverse_start_y)**2) >= 0.1):
                self.stop_motors()
                if (self.goal_count == -1):
                    self.rotate(45)
                elif (self.goal_count == -2):
                    self.rotate(90)
                self.goal_count = 4  # return to wall following


        self.rotate_to_goal()
        self.compute_position
        self.d_goal_dist = -1
        self.speed = 50
        self.run_tank(self.speed)
        wait(500)

        while (self.d_goal_dist <=0): 
            self.compute_position()
            print("{},{}".format(self.x, self.y))
            print(self.d_goal_dist)

        self.stop_motors() 

        while(abs(self.theta % 360 - 90) > 0.1):
            error = (90 - (-self.gyroscope.angle())) % 360
            if error > 180:
                error -= 360
            self.rotate(-error)
            self.compute_position()

        self.ev3.speaker.beep(frequency=800, duration=400)
        print(self.goal_dist)

                



def main():
    lab4 = MyController()
    lab4.run()


if __name__ == "__main__":
    main()



