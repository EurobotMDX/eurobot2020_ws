#!/usr/bin/env python

import json
import rospy
import signal
from std_msgs.msg import String, Bool

import serial

DEFAULT_PORT = "/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0"
DEFAULT_BAUD = 115200
DEFAULT_LOOP_RATE = 10

class SerialDataHandler(object):
    def __init__(self, default_port=DEFAULT_PORT, default_baud=DEFAULT_BAUD, default_loop_rate=DEFAULT_LOOP_RATE):
        self.port = self.default_port = default_port
        self.baud = self.default_baud = default_baud
        self.loop_rate = self.default_loop_rate = default_loop_rate

        self.rate = None
        self.serial_device = None

        self._data_buffer = ""

        self.range_data_pub = rospy.Publisher('raw_range_data', String, queue_size=5)
        self.p2s_pub = rospy.Publisher('pull_to_start', Bool, queue_size=5)
        self.msg_subscriber  = rospy.Subscriber('serial_data_handler_msg', String, self.msg_received)

        self.is_killed = False
        self.should_run = True

        rospy.init_node('serial_com_data_handler', anonymous=False)
    
    def initialize(self):
        # self.port = rospy.get_param('serial_port', self.default_port)
        # self.baud = rospy.get_param('serial_baud', self.default_baud)
        # self.loop_rate = rospy.get_param('loop_rate', self.default_loop_rate)
        
        if self.serial_device is None:
            try:
                self.serial_device = serial.Serial(self.port, self.baud, timeout=0.1)
            except:
                rospy.loginfo("could not connect to serial device")
        
        if self.serial_device is not None:
            self.rate = rospy.Rate(self.loop_rate)
            self.is_killed = False
    
    def terminate(self):
        if self.serial_device is not None:
            self.serial_device.close()
            self.serial_device = None
        
        self.is_killed = True

    def kill(self):
        rospy.loginfo("[INFO] killing the serial manager")
        self.should_run = False
        self.terminate()
    
    def reset(self, wait_interval=1.0):
        rospy.loginfo("resetting serial device")
        self.terminate()

        rospy.sleep(wait_interval)
        self.initialize()
    
    def msg_received(self, msg):
        if (self.serial_device is None) or (self.is_killed):
            rospy.loginfo("[INFO] Arduino is not connected")
            return

        # rospy.loginfo("[INFO] serial manager is sending {} to the arduino".format(msg.data))
        
        try:
            self.serial_device.write(str(msg.data))
        except:
            rospy.loginfo("could not write to serial device")
            self.reset()

    def read_data_buffer(self):
        if (self.serial_device is None) or (self.is_killed):
            return None

        try:
            return self.serial_device.readlines()
        except KeyboardInterrupt:
            rospy.loginfo("setting serial device should_run var to False")
            self.should_run = False
        except:
            rospy.loginfo("could not read from serial device")
            rospy.sleep(1.0)

            if (self.serial_device is None) or (self.is_killed):
                rospy.loginfo("serial device is not active")
            else:
                self.reset()

    def run(self):
        while (not rospy.is_shutdown()) and self.should_run:
            data  = self.read_data_buffer()

            if isinstance(data, list):
                if len(data) > 0:
                    try:
                        data = json.loads(data[-1].strip("\r\n"))
                        self.range_data_pub.publish(str(data["d"]))
                        self.p2s_pub.publish(data["p2s"])
                    except:
                        rospy.loginfo("Error processing serial message")
                        rospy.loginfo(data)

            self.rate.sleep()


def main():
    rospy.sleep(10)
    my_serial_manager = SerialDataHandler()
    my_serial_manager.initialize()
    
    try:
        my_serial_manager.run()
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        my_serial_manager.kill()

    my_serial_manager.kill()

    

if __name__ == '__main__':
    main()
