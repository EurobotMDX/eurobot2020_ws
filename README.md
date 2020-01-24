![Brainstorm Robotics Logo](http://www.brainstorm.mdx.ac.uk/wp-content/uploads/2018/07/LOGO-BRAINSTRORM-05.png?raw=true "Middlesex University of London")


* [http://brainstorm.mdx.ac.uk](http://brainstorm.mdx.ac.uk) - official team website, visit to meet the team!



# EUROBOT 2020 WORKSPACE

Repository exclusively for team Brainstorm - Middlesex University of London

All rights reserved © 2020, London, UK


# GETTING STARTED

These instructions will get you a copy of the Eurobot project up and running on your local machine for development and testing purposes. See ROS Documentation section for notes on how to deploy and run the project on a Linux.

## Prerequisites

What things you need to install the software and how to install them

* [Ubuntu MATE for the Raspberry Pi - web](https://ubuntu-mate.org/download/) - Download Ubuntu MATE for Raspberry Pi
* [Ubuntu MATE for the Odroix XU-04 - web](https://wiki.odroid.com/odroid-xu4/odroid-xu4) - Download Ubuntu MATE for Odroid XU-04

## DATE/TIME on Odroid - if system and hardware date/time is wrong then must be set to current date/time
to check date use ```date```
to check hardware date use ```sudo hwclock```

Don't commit any changes to github repo if the date n time is not set correctly

## Versioning

For the versions available, see the tags of this repository and selected branches according to your role in the team.
Keep code clean and leave comments in code or/and write brief documentation after each new feature deployed.



# SYSTEM REQUIREMENTS
* ROS Kinetic ONLY supports Ubuntu 16.04
* [Ubuntu MATE ISO image to download for ODROID](https://wiki.odroid.com/odroid-xu4/odroid-xu4)
* Open SSH - to establish remote connection 
* GIT - for version control 
* .bashrc file must be edited beforehand in order to run ROS locally on your PC (see section 'ROS: Installation' )




# ROS DOCUMENTATION:

## Getting started with ROS [Robot Operating System]

### Installation
* [Ubuntu install of ROS Kinetic RECOMMENDED - wiki.ros tutorial](http://wiki.ros.org/kinetic/Installation/Ubuntu) - Installation process in steps
* [Shell script .sh installing ROS automaticly NOT RECOMMENDED FOR BEGINNERS](https://github.com/chibike/shell_scripts/blob/master/install_ros_kinetic_com.sh)



### Edit bashrc in order to run ROSCORE
Environment setup
* ROS environment variables are automatically added to your bash session every time a new shell is launched
```
echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
* If you have more than one ROS distribution installed, ~/.bashrc must only source the setup.bash for the version you are currently using.

* If you just want to change the environment of your current shell, instead of the above you can type:
```
source /opt/ros/kinetic/setup.bash
```

### Usage
You must have a roscore running in order for ROS nodes to communicate. It is launched using the roscore command.
```
roscore
```
* Run ROS in separate terminal and let it be running in the background
* It can be only one instance of ROS running on machine 
* To terminate or close safely roscore, in the active terminal type:
> CTRL + C

### References, knowledgebase
* [ROS Cheat Sheet](https://w3.cs.jmu.edu/spragunr/CS354/handouts/ROSCheatsheet.pdf)
* [ROS V-Useful Tutorials for begginers - explore wiki.ros with tutorials](http://wiki.ros.org/ROS/Tutorials)
* [ROS communication with Arduino - setup, sensors and much more tuts](http://wiki.ros.org/rosserial_arduino/Tutorials)
* [Programming Robots with ROS O'Reilly - 427 pages eBook for download](http://marte.aslab.upm.es/redmine/files/dmsf/p_drone-testbed/170324115730_268_Quigley_-_Programming_Robots_with_ROS.pdf)



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
* restarting service using bash alias (if created)
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
List of supported topic commands: (ordered by importance)
```
rostopic list   print information about active topics
rostopic info <topic-name>  print information about active topic
rostopic echo /topic_name  or /my_topic/field_name   print messages to screen
rostopic pub /topic_name std_msgs/String hello   publish data to topic
rostopic type /topic_name  print topic type
rostopic hz /topic_name    display publishing rate of topic
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
* other launch files running packages/nodes individually or partially 
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


# ROBOT DRIVERS:
Low level code in C++, not need to be changed at all. After every change in code needs to be recompiled by catkin_make
## FOLDER "Includes"
### FILE drive_train_manager.h 
Class DriveTrainManager defines methods related with driving include headers from robot_params.h 
```
set_motion()
reset_encoders()
reset_values()
stop()
set_velocity()
update_odometry()
current_x
current_y

```
* defines EPOS objects assigned to the wheels, includes headers from epos_drive_manager.h 
```
 // epos objects
EposDriveManager left_wheel;
EposDriveManager right_wheel;
```
### FILE epos_drive_manager.h 
Class EposDriveManager methods and definitions
```
initialize(const std::string device_name, const std::string port_name);
terminate() 
reset() 
set_rpm(const int motor_rpm) 
increment_position(const long delta_position) 
get_rpm(int &motor_rpm) 
get_position(int &motor_position) 
reset_encoders() 
stop() // apply brakes to the wheels

// return true if encoder is ineserted .set_inverted when creating object EPOS method
set_inverted();
reset_inverted();
```
### FILE robot_params.h
Constance definitions of key paramiters for driving
```
// using meters, radians, etc. meteric only!
_RB_BASE_WIDTH 0.1714 // to contact center of wheels need to be changed as well
_RB_WHEEL_DIAMETER 0.07
_RB_NUM_OF_ENCODER_COUNTS 16384 // 4096 * 4 // old value
_RB_ABS_GEAR_RATIO (4554.0 / 130.0) // need to be chaged to 1
_RB_INVERT_RIGHT true // find out does it need to be changed or not
```
### FILE drive_train_ros_handler.h 
* Includes (imports) all nessesery libraries and header files and the Thread. Contains ROS C++ library

## FOLDER "Src"

### FILE robot_interface.py
Basic driving methods

### FILE robot_interface_advanced.py
Extension for Class robot_interface with more advanced driving methods

## FOLDER "Script"

### FILE epos_drive_manager.cpp - EposDriveManager() object
* contains entire logic of methods defined in epos_drive_manager.h, manages EPOS devices and calculates PIDs

### FILE drive_train_ros_handler.cpp
* it uses callbacks listaning on topics for subcribers
* Set the publish rate for Publishers, change according to performance (now it's 10)
```
int publish_rate;
	nh.param<int>("publish_rate", publish_rate, 10)
 ```
 * creates the ROS Subscribers:
 ```
 /cmd_vel
 /cmd_vel_mux/input/teleop
 /reset_drive_train
 /initialpose
 /update_drive_train_position
 ```
 * creates the ROS Publisher
 ```
 /odom
 ```
 * runs the odometry thread which publish data in while loop to /odom
 ```
 thread odometry_update_loop(odometry_loop)
 ```
 

### FILE drive_train_manager.cpp
* DriveTrainManager instantiation with assigning EPOS devices to "USB0" and "USB1" port
* Creation and functionality of wheel objects
```
left_wheel  = EposDriveManager();
right_wheel = EposDriveManager();
```
* _RB_INVERT_RIGHT - inverssion of the wheel according to robot build
* DriveTrainManager::update_odometry() - calculations of driving odometry 


# Electronic parts list:

# FAQ
* In case of Arduino crash - restart the service
* After creating python script make it executable with command: chmod +x script.py 
* I can't compile with catkin_make: 
⋅⋅⋅If you want to compile something you need to update the clock (time)
⋅⋅⋅You must navigate to main workspace directory while you run the command



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

<i>Our Credo: Show up, Deliver, Be Kind, Repeat</i>
