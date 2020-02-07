#!/usr/bin/env python

import thread
import time
import rospy, signal
from std_msgs.msg import String

SHOULD_RUN = False
THREAD_LOCKED = False


def do_generic():
    global SHOULD_RUN
    rospy.loginfo("Do generic")
    rospy.sleep(0.5)

def table_blue():
    global SHOULD_RUN
    rospy.loginfo("Starting blue side")
    rospy.sleep(0.5)

def table_yellow():
    global SHOULD_RUN
    rospy.loginfo("Starting yellow side")
    rospy.sleep(0.5)

def test_robot():
    global SHOULD_RUN
    rospy.loginfo("Testing the robot")
    rospy.sleep(0.5)

def eurobot_task_cmd_handler():
    global SHOULD_RUN, THREAD_LOCKED
    rospy.loginfo("Received the command")
    rospy.sleep(0.5)

def eurobot_task_cmd_callback():
    global THREAD_LOCKED
    rospy.loginfo("Received the command")
    rospy.sleep(0.5)



rospy.loginfo("ctrl-c to terminate")
rospy.spin()
rospy.loginfo("terminating....")