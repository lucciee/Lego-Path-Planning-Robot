[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/rXLLujPm)

## The Objective
Assembling and programing a wheeled robot capable of moving as quickly as possible from a start
location to a known goal location in an unknown environment while avoiding static obstacles.

## Robot Design Constraints
The robot is built only using components from a Lego Mindstorms kit. The robot is designed to traverse a 400 cm x 400 cm workspace autonomously
without any human intervention. The workspace will include various unknown obstacles for the robot to circumnavigate as will as a target coordinate for the robot to reach. The robot is allowed to make contact with obstacles. Leaving the workspace is not permitted. 
<img width="918" height="616" alt="Screenshot 2026-09-15 173317" src="https://github.com/user-attachments/assets/6dad19b8-2346-405e-9ebf-08861ae37054" />


## Robot features
  2 Front Rubber Wheels and motors     (steering and locomotion)  
  1 Rear Caster Wheel                  (support point for balance)  
  Gyroscope                            (dead reckoning)  
  2 Bumper Sensors                     (tactile object detection)  
  Ultrasonic Sensor                    (distant object detection)  
  Speakers                             (plays fanfare when goal is reached)  
<img width="740" height="662" alt="Screenshot 2026-09-15 172429" src="https://github.com/user-attachments/assets/c4e7b2dd-cc53-4fee-8841-e32f34513a57" />
<img width="724" height="668" alt="Screenshot 2026-09-15 172423" src="https://github.com/user-attachments/assets/e1b4400d-3b4c-450e-954a-5bfde370891a" />


## Path Planning Algorithm
The robot's path is determine using an algorithm based on the **Bug 2 Algorithm**, where an imaginary line called the **m-line** is drawn between the start and goal coordinates. The robot follows this m-line until it encounters an obstacle, at which point it records its location as an **hit point**. The robot then circumnavigates the obstacle's perimeter until it reencounters the m-line. This process is repeated until the goal is reached.

Adjustments were made to the standard Bug 2 Algorithm to account for suboptimal and inaccurate sensor readings and motor functions. For example, the Ultrasonic sensor equipped on the robot appeared to give faulty reading, requiring the robot to rely more heavily on tactile feedback from the Bumper sensors. 

<img width="641" height="477" alt="image" src="https://github.com/user-attachments/assets/b489ba53-6057-4aab-82a6-71de589d7504" />


### Uploading the code onto the Lego Mindstorms EV3

1. Plug robot to computer using USB cable.
2. In the VSCode Explorer open the EV3DEV DEVICE BROWSER.
3. Click `Click here to connect to a device`.
4. Select your device from the list.
5. To run your code while viewing the terminal output, click Run -> Start Debugging or F5 or click Run -> Run Without Debugging or Ctrl + F5 (Cmd + F5 on Mac).
6. You may also upload the code to the robot and edit the directories on the robot via the EV3DEV DEVICE BROWSER.


