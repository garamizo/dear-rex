#!/usr/bin/env python
import rospy
from geometry_msgs.msg import TwistStamped
import RPi.GPIO as IO
import numpy as np


class RabbitMotor:
    PIN_IN1 = 2
    PIN_IN2 = 3
    PIN_EN1 = 4
    PIN_IN3 = 17
    PIN_IN4 = 27
    PIN_EN2 = 22

    def __init__(self):

        IO.setmode(IO.BCM)
        IO.setup(self.PIN_IN1, IO.OUT)
        IO.setup(self.PIN_IN2, IO.OUT)
        IO.setup(self.PIN_IN3, IO.OUT)
        IO.setup(self.PIN_IN4, IO.OUT)
        IO.setup(self.PIN_EN1, IO.OUT)
        IO.setup(self.PIN_EN2, IO.OUT)

        self.en1 = IO.PWM(self.PIN_EN1, 100)
        self.en2 = IO.PWM(self.PIN_EN2, 100)

    def write(self, ur, ul):
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
    rospy.Subscriber('/rabbit_velocity_controller/cmd_vel_out', TwistStamped, twist_cb)
    rabbit = RabbitMotor()

    rospy.spin()
    IO.cleanup()
