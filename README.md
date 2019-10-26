![Brainstorm Robotics Logo](http://www.brainstorm.mdx.ac.uk/wp-content/uploads/2018/07/LOGO-BRAINSTRORM-01.png?raw=true "Middlesex University of London")

*[http://brainstorm.mdx.ac.uk](http://brainstorm.mdx.ac.uk) - official team website, visit to meet the team!


# Eurobot2020 WORKSPACE

Repository exclusively for team Brainstorm - Middlesex University

All right reserved 2019-2020
Middlesex University of London


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```
* [Ubuntu MATE for the Raspberry Pi - web](https://ubuntu-mate.org/download/) - Download Ubuntu MATE for Raspberry Pi
* [Ubuntu MATE for the Odroix XU-04 - web](https://wiki.odroid.com/odroid-xu4/odroid-xu4) - Download Ubuntu MATE for Odroid XU-04
* [Ubuntu install of ROS Kinetic - web](http://wiki.ros.org/kinetic/Installation/Ubuntu) - Installation process in steps

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Versioning

For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 


# System Requirements

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

## ROS Packages 

### Package: Upstart for ROS Robots
This package aims to assist with creating simple platform-specific jobs to start your robot’s ROS launch files as a service when its PC/ROBOT powers up.

#### Installation
The basic usage is with the install script, which can be as simple as:
```
rosrun robot_upstart install eurobot_bringup/launch/base.launch
```

This will create a job called eurobot on your machine, which launches base.launch. It will start automatically when you next start your machine. 

### Usage
You can bring it up and down manually:

```
sudo service eurobot_bringup start
sudo service eurobot_bringup stop
sudo service eurobot_bringup restart

```
restarting service using alias
```
sudo ./restart_eurobot_service.sh 
```


### Package: Turtle Bot for driving using controls
Provides teleoperation using joysticks or keyboard.

#### Installation
* [The turtlebot stack provides all the basic drivers for running and using a TurtleBot with ROS.](https://github.com/turtlebot/turtlebot)

#### Usage
```
roslaunch turtlebot_teleop keyboard_teleop.launch 
```
### Package: eurobot_bringup

### Package: navigation

### Package: robot_description

### Package: robot_drivers

### Package: robot_grippers

### Package: robot_vision

### Package: sensor_drivers

### Package: web_server

### Package: world_description

## ROS Nodes

## ROS Topics

## ROS Files

# Network configuration:



# Robot scripts:


# Robot drivers:



# Electronic parts list:



# Contributors:



# Sponsors:
- FESTO
- Maxon Motors
- Rapid Electronics
- PozyX


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
