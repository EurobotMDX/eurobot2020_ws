#!/usr/bin/env python

import os
import rospy
from std_msgs.msg import String, Bool, Float32
from sensor_msgs.msg import Range
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

from tf.transformations import euler_from_quaternion, quaternion_from_euler

import json
from server import *

def __log(status="INFO", message=""):
    rospy.loginfo("[{status}] {message}".format(status=status, message=message))

__log("initializing node {}".format(NODE_NAME))


rospy.init_node("{}".format(NODE_NAME), anonymous=False)
rospy.on_shutdown(shutdown_server)

robot_position = {
            "x"   : 0.0,
            "y"   : 0.0,
            "yaw" : 0.0
        }

pull_to_start_state = True
robot_score = 0.0
    
def pull_to_start_callback(msg):
    global pull_to_start_state

    pull_to_start_state = msg.data

rospy.Subscriber('pull_to_start', Bool, pull_to_start_callback)

def robot_score_callback(msg):
    global robot_score

    robot_score = msg.data

rospy.Subscriber('robot_score', Float32, robot_score_callback)

def update_robot_position(odometry_msg):
    robot_pose = odometry_msg.pose.pose

    _, _, robot_position["yaw"] = euler_from_quaternion([robot_pose.orientation.x, robot_pose.orientation.y, robot_pose.orientation.z, robot_pose.orientation.w])
    robot_position["x"] = robot_pose.position.x
    robot_position["y"] = robot_pose.position.y

#["{s,0,0}{s,1,3.14}", "{s,0,1}{s,1,.8}", "{s,0,0}{s,1,3.14}"]
serial_data_pub = rospy.Publisher('serial_data_handler_msg', String, queue_size=10)
reset_drive_train_pub = rospy.Publisher('/reset_drive_train', Bool, queue_size=10)
eurobot_task_cmd_pub = rospy.Publisher('/eurobot_task_cmd', String, queue_size=10)

rospy.Subscriber("odom", Odometry, update_robot_position)

@app.route("/reset_task")
def reset_task():
    eurobot_task_cmd_pub.publish(String("reset"))
    return "Reseting Task"

@app.route("/test_robot")
def test_robot():
    try:
        side = request.args.get("side").decode("utf-8")
        cmd = "test_{}".format(side)
        rospy.loginfo("testing with command {}".format(cmd))
        eurobot_task_cmd_pub.publish(String(cmd))
    except:
        pass
        
    return "Testing Robot"

@app.route("/start_task")
def start_task():

    try:
        side = request.args.get("side").decode("utf-8")
        cmd = "start_{}".format(side)
        rospy.loginfo("starting side with command {}".format(cmd))
        eurobot_task_cmd_pub.publish(String(cmd))
    except:
        pass
    
    return "Starting Task"

@app.route("/shutdown")
def shutdown():
    rospy.loginfo("[INFO] Shutting Down")

    os.system("sh /home/odroid/scripts/shutdown_script.sh &")
    os.system("disown")
    rospy.loginfo("[INFO] shutting down now....")
    return "Shutting Down"

@app.route("/eurobot_task_reset")
def eurobot_task_reset():
    msg = String()
    msg.data = "reset"
    eurobot_task_cmd_pub.publish(msg)
    return "Eurobot Task Reset"

@app.route("/eurobot_kill_task")
def eurobot_kill_task():
    msg = String()
    msg.data = "kill_task"
    eurobot_task_cmd_pub.publish(msg)
    return "Eurobot Kill Task"

@app.route("/eurobot_start_yellow")
def eurobot_start_yellow():
    msg = String()
    msg.data = "start_yellow"
    eurobot_task_cmd_pub.publish(msg)
    return "Eurobot Start Task Yellow"

@app.route("/eurobot_start_purple")
def eurobot_start_purple():
    msg = String()
    msg.data = "start_purple"
    eurobot_task_cmd_pub.publish(msg)
    return "Eurobot Start Task Purple"

@app.route("/reset_odometry")
def reset_odometry():
    msg = Bool()
    msg.data = True
    reset_drive_train_pub.publish(msg)
    return "Odometry Reset"

@app.route("/get_robot_position")
def get_robot_position():
    return json.dumps(robot_position)

@app.route("/get_robot_score")
def get_robot_score():
    global robot_score
    
    data = {"s":robot_score}
    return json.dumps(data)

@app.route("/get_pull_to_start")
def get_pull_to_start():
    global pull_to_start_state

    data = {"p2s":pull_to_start_state}
    return json.dumps(data)

@app.route("/open_gripper")
def open_gripper():
    msg = String()
    msg.data = "{s,0,0.4}{s,1,1.4}" #"{s,0,0}{s,1,3.14}"
    serial_data_pub.publish(msg)
    return "Gripper Opened"

@app.route("/close_gripper")
def close_gripper():
    msg = String()
    msg.data = "{s,0,0.8}{s,1,1.0}" #"{s,0,1}{s,1,.8}"
    serial_data_pub.publish(msg)
    return "Gripper Closed"

@app.route("/push_left")
def push_left():
    msg = String()
    msg.data = "{s,2,2.2}"
    serial_data_pub.publish(msg)
    return "Pushing Left"

@app.route("/push_right")
def push_right():
    msg = String()
    msg.data = "{s,2,0.6}"
    serial_data_pub.publish(msg)
    return "Pushing Right"

@app.after_request
def allow_cors(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

__log("Starting web server")
thread.start_new_thread(app.run, (HOST, PORT))

time.sleep(5)
__log("Server should be running")

rospy.spin()

