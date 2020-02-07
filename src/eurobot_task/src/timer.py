#!/usr/bin/env python

import time
import rospy

from std_msgs.msg import String

def stopwatch(seconds):
    start = time.time()
    time.clock()
    elepsed = 0
    while elepsed < seconds:
        elepsed = time.time() - start
        rospy.loginfo("loop cycle time: %f, seconds count: %02d" % (time.clock(), elepsed))
        pub.publish(data="time elapsed: %02d" % elepsed)
        time.sleep(1)

if __name__ == "__main__":
     while not rospy.is_shutdown():
        rospy.init_node("task_timer", anonymous=False, disable_signals=True)
        pub = rospy.Publisher('time_elapsed',String , queue_size=10)

        stopwatch(10)

        rospy.loginfo("ctrl-c to terminate")
        rospy.spin()
        rospy.loginfo("terminating....")
    

