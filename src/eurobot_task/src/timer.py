#!/usr/bin/env python

import time
import rospy

from std_msgs.msg import String
from geometry_msgs.msg import Twist




def stopwatch(seconds):
    start = time.time()
    time.clock()
    elepsed = 0
    while elepsed < seconds:
        elepsed = time.time() - start
        rospy.loginfo("loop cycle time: %f, seconds count: %02d" % (time.clock(), elepsed))
        pub.publish(data="time elapsed: %02d" % elepsed)
        time.sleep(1)


        
def shutdown():
    # Always stop the robot when shutting down the node.
    rospy.loginfo("Stopping the robot...")
    cmd_vel.publish(Twist())
    rospy.sleep(1)

    


if __name__ == '__main__':
    try:
        # Give the node a name
        rospy.init_node("task_timer", anonymous=False, disable_signals=True)
        cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
        
        pub = rospy.Publisher('time_elapsed',String , queue_size=10)
        stopwatch(10)


        # Set rospy to execute a shutdown function when exiting
        rospy.on_shutdown(shutdown)

        # Stop the robot.
        cmd_vel.publish(Twist())
        
        shutdown()
        
    except rospy.ROSInterruptException:
        rospy.loginfo("Timer node terminated.")





# if __name__ == "__main__":
#      while not rospy.is_shutdown():
        
        

#         rospy.loginfo("ctrl-c to terminate")
#         rospy.spin()
#         rospy.loginfo("terminating....")
    

