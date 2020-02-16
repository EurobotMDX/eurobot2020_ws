#!/usr/bin/env python
import rospy
import sys
from geometry_msgs.msg import Twist
 
def publish_velocity_commands():
  # Velocity publisher
  vel_pub = rospy.Publisher('/ubot/base_controller/cmd_vel', Twist, queue_size=10)
  rospy.init_node('ubot_simple_twist_pub', anonymous=True)
 
  msg = Twist()
  msg.linear.x = 0.1
  msg.linear.y = 0
  msg.linear.z = 0
  msg.angular.x = 0
  msg.angular.y = 0
  msg.angular.z = 0
 
  rate = rospy.Rate(10) # 10hz
  while not rospy.is_shutdown():
    vel_pub.publish(msg)
    rate.sleep()
 
if __name__ == '__main__':
  if len(sys.argv) == 1:
    try:
      publish_velocity_commands()      
    except rospy.ROSInterruptException:
      pass
  else:
    print("Usage: rosrun ubot_simple_control ubot_simple_twist_pub.py")
