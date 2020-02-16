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
time_elapsed = "0"
    
def pull_to_start_callback(msg):
    global pull_to_start_state

    pull_to_start_state = msg.data

rospy.Subscriber('pull_to_start', Bool, pull_to_start_callback)

def robot_score_callback(msg):
    global robot_score

    robot_score = msg.data

rospy.Subscriber('robot_score', Float32, robot_score_callback)



def update_time_elapsed(msg):
    global time_elapsed

    time_elapsed = msg.data

rospy.Subscriber('time_elapsed', String, update_time_elapsed)



def update_robot_position(odometry_msg):
    robot_pose = odometry_msg.pose.pose

    _, _, robot_position["yaw"] = euler_from_quaternion([robot_pose.orientation.x, robot_pose.orientation.y, robot_pose.orientation.z, robot_pose.orientation.w])
    robot_position["x"] = robot_pose.position.x
    robot_position["y"] = robot_pose.position.y

serial_data_pub = rospy.Publisher('serial_data_handler_msg', String, queue_size=10)
# reset_drive_train_pub = rospy.Publisher('/reset_drive_train', Bool, queue_size=10)
# eurobot_task_cmd_pub = rospy.Publisher('/eurobot_task_cmd', String, queue_size=10)

# rospy.Subscriber("odom", Odometry, update_robot_position)

rospy.Subscriber("/ubot/base_controller/odom", Odometry, update_robot_position)




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


@app.route("/get_time_elapsed")
def get_time_elapsed():
    global time_elapsed
    
    data = {"time":time_elapsed}
    return json.dumps(data)



@app.after_request
def allow_cors(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

__log("Starting web server")
thread.start_new_thread(app.run, (HOST, PORT))

time.sleep(5)
__log("Server should be running")

rospy.spin()

