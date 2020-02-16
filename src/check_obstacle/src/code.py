import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def callback(msg):
	print(msg.ranges[360])
	move.linear.x=0.1
	if msg.ranges[360] <1:
		move.linear.x = 0
	pub.publish(move)

rospy.init_node('check_obstacle')
sub = rospy.Subscriber('ubot/laser/scan', LaserScan, callback)
pub = rospy.Publisher('/cmd_vel', Twist)
move = Twist()

rospy.spin()
