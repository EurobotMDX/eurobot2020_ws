![Brainstorm Robotics Logo](http://www.brainstorm.mdx.ac.uk/wp-content/uploads/2018/07/LOGO-BRAINSTRORM-01.png?raw=true "Middlesex University of London")

* [http://brainstorm.mdx.ac.uk](http://brainstorm.mdx.ac.uk) - official team website, visit to meet the team!


# EUROBOT 2020 WORKSPACE

Repository exclusively for team Brainstorm - Middlesex University of London

All rights reserved © 2020, London, UK


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

* [Ubuntu MATE for the Raspberry Pi - web](https://ubuntu-mate.org/download/) - Download Ubuntu MATE for Raspberry Pi
* [Ubuntu MATE for the Odroix XU-04 - web](https://wiki.odroid.com/odroid-xu4/odroid-xu4) - Download Ubuntu MATE for Odroid XU-04
* [Ubuntu install of ROS Kinetic - web](http://wiki.ros.org/kinetic/Installation/Ubuntu) - Installation process in steps

### Installing

A step by step series of examples that tell you how to get a development env running


## Versioning

For the versions available, see the tags of this repository and selected branches 


# System Requirements
* ROS Kinetic ONLY supports Ubuntu 16.04
* [Ubuntu MATE ISO image, Wiki-page for ODROID](https://wiki.odroid.com/odroid-xu4/odroid-xu4)
* OPEN SSL
* GIT



# ROS documentation:

## Running the ROS

Explanation how to run the ROS

* [ROS Kinetic for Ubuntu - wiki.ros tutorial](http://wiki.ros.org/kinetic/Installation/Ubuntu)
* [ROS V-Useful Tutorials for begginers - explore wiki.ros with tutorials](http://wiki.ros.org/ROS/Tutorials)
* [ROS communication with Arduino - setup, sensors and much more tuts](http://wiki.ros.org/rosserial_arduino/Tutorials)
* [Programming Robots with ROS O'Reilly - 427 pages eBook for download](http://marte.aslab.upm.es/redmine/files/dmsf/p_drone-testbed/170324115730_268_Quigley_-_Programming_Robots_with_ROS.pdf)
* [ROS Cheat Sheet](https://w3.cs.jmu.edu/spragunr/CS354/handouts/ROSCheatsheet.pdf)

## ROS PACKAGES
### Usage
Provides package list and info
```
rospackage list
rospackage name_pkg info
```

Run this to provide dependecies to any script. 
<b>Minimal.launch provides basic robot functions essential to run any script in order of testing and development </b>
```
roslaunch pckg_name launch_file_name 
roslaunch eurobot_bringup minimal.launch
```

### PACKAGE Upstart for ROS Robots
This package aims to assist with creating simple platform-specific jobs to start your robot’s ROS launch files as a service when its PC/ROBOT powers up.

#### Installation
```
sudo apt-get install ros-kinetic-robot-upstart
```
* install YOUR launch file [within the src folder]
```
#rosrun robot_upstart install eurobot_bringup/launch/minimal.launch rosrun robot_upstart install eurobot_bringup/launch/minimal.launch --job eurobot_bringup --user root --rosdistro kinetic --logdir eurobot_bringup/logs
```
* to complete the installation 
```
sudo systemctl daemon-reload && sudo systemctl start eurobot
```
* to view output to terminal
```
sudo tail /var/log/upstart/eurobot.log -n 30
```


#### Usage
* The basic usage is with the install script, which can be as simple as:
```
rosrun robot_upstart install eurobot_bringup/launch/base.launch
```

This will create a job called eurobot on your machine, which launches base.launch. It will start automatically when you next start your machine. 

* You can bring it up, down and restart manually:

```
sudo service eurobot_bringup start
sudo service eurobot_bringup stop
sudo service eurobot_bringup restart

```
restarting service using bash alias (if created)
```
sudo ./restart_eurobot_service.sh 
```


### PACKAGE Turtle Bot for driving using controls
Provides teleoperation using joysticks or keyboard.

#### Installation
* [The turtlebot stack provides all the basic drivers for running and using a TurtleBot with ROS.](https://github.com/turtlebot/turtlebot)

#### Usage
```
roslaunch turtlebot_teleop keyboard_teleop.launch 
```
### PACKAGE eurobot_bringup

### PACKAGE navigation

### PACKAGE robot_description

### PACKAGE robot_drivers

### PACKAGE robot_grippers

### PACKAGE robot_vision

### PACKAGE sensor_drivers

### PACKAGE web_server

### PACKAGE world_description

## ROS NODES
### Usage
Provides list and info of nodes
```
rosnode list
rosnode node_name info
```

### NODE /drive_train_controller  - driving systems, braking systems, odometry
### NODE /range_sensors_ros_handler_node - ultrasonic sensors
### NODE /robot_state_publisher - publishes robot states - ex for rviz
### NODE /serial_com_data_handler - Serial port connections 
### NODE /web_server_node - Flask

## ROS TOPICS
### Usage
Check what topics are available in ROS
```
rostopic list 
```

## ROS FILES


### FILE robot_drivers/script/robot_interface.py
Class required to minimal run contain all necessary APIs for grippers, experiment, update_robot_score, wait_for_pull_to_start, reset_odometry
> need to be initiate

### FILE robot_drivers/script/robot_interface_advanced.py
Class with inherited methods from robot_interface.py, contains all methods need for driving to the point, waypoints, get_distance, move_linear, move_angular, move_to, 
> need to be initiate

### FILE robot_drivers/script/eurobot_task.py
Import all robot_interface_advanced.py methods and is the main file with driving commands for a small robot

#### Usage
Commands available in eurobot_task.py :
```
robot.update_robot_score(40.0)
robot.open_gripper()
robot.close_gripper()
robot.stop_motors()
```
## LAUNCH Files:
Provide convenient way to start up multiple nodes and a master, as well as other initialization requirements such as setting parameters.
### Usage
```
eurobot_bringup/launch/Eurobot_final.launch
```
other launch files running packages/nodes individually or partially 
```
-> minimal.launch
-> nodepkg=”robot_drivers”
-> nodepkg=”robot_state_publisher”
-> sensors.launch
-> web_server.launch
-> eurobot_task.launch 
-> eurobot_task.py
```

# Network configuration:



# Robot scripts:


# Robot drivers:



# Electronic parts list:

# FAQ
* In case of Arduino crash - restart the service
* After creating python script make it executable with command: chmod +x script.py 
* I can't compile with catkin_make: 
... If you want to compile something you need to update the clock (time)
... You must navigate to main workspace directory while you run the command



# Contributors:
* Visit http://brainstorm.mdx.ac.uk to meet the team


# Sponsors:
- FESTO
- Maxon Motors
- Rapid Electronics
- PozyX


# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

# Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
