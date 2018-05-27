#!/usr/bin/env python
import rospy
from geometry_msgs.msg import TwistStamped
import RPi.GPIO as IO
import numpy as np


class RexMotor:
    PIN_ENA = 3
    PIN_IN1 = 5
    PIN_IN2 = 7
    PIN_IN3 = 11
    PIN_IN4 = 13
    PIN_ENB = 15

    def __init__(self):

        IO.setmode(IO.BOARD)
        IO.setup(self.PIN_ENA, IO.OUT)
        IO.setup(self.PIN_IN1, IO.OUT)
        IO.setup(self.PIN_IN2, IO.OUT)
        IO.setup(self.PIN_IN3, IO.OUT)
        IO.setup(self.PIN_IN4, IO.OUT)
        IO.setup(self.PIN_ENB, IO.OUT)

        self.en1 = IO.PWM(self.PIN_ENA, 100)
        self.en2 = IO.PWM(self.PIN_ENB, 100)

        IO.output(self.PIN_IN1, IO.HIGH)
        IO.output(self.PIN_IN2, IO.LOW)

    def write(self, ur, ul):
        print("%.2f %.2f" % (ur, ul))
        ur = np.clip(ur, -100, 100)
        ul = np.clip(ul, -100, 100)

        IO.output(self.PIN_IN1, IO.HIGH if ul < 0 else IO.LOW)
        IO.output(self.PIN_IN2, IO.LOW if ul < 0 else IO.HIGH)
        self.en1.start(abs(ul))

        IO.output(self.PIN_IN3, IO.HIGH if ur < 0 else IO.LOW)
        IO.output(self.PIN_IN4, IO.LOW if ur < 0 else IO.HIGH)
        self.en2.start(abs(ur))


def twist_cb(msg):
    right = 100 * msg.twist.linear.x + 100 * msg.twist.angular.z
    left = 100 * msg.twist.linear.x - 100 * msg.twist.angular.z
    rabbit.write(right, left)


if __name__ == "__main__":

    rospy.init_node('simple_nav', anonymous=True)
    rospy.Subscriber('/rex_velocity_controller/cmd_vel_out', TwistStamped, twist_cb)
    rabbit = RexMotor()

    rospy.spin()
    IO.cleanup()
