#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import sensor_msgs.msg
import random
import numpy as np
from geometry_msgs.msg import Twist
from itertools import *
from operator import itemgetter

LINX = 0.0 #Always forward linear velocity.
PI = 3.14
angz = 0
L=0
R=0
F=0

def SonarFScan(data):
    global F
    global LINX
    global angz
    try:
        F = data.range
        if(F<=0.3):
            LINX = LINX/2 
            if L-R<0.1:
                angz= angz+0.1
    except Exception as err:
        print(err)

def SonarLScan(data):
    global L
    global angz
    try:
        L = data.range
        
        if(L<0.3):
            angz= angz+0.1
        else: angz=angz
    except Exception as err:
        print(err)

def SonarRScan(data):
    global R
    global angz
    try:
        R = data.range
        if(R<0.3):
            angz= angz-0.1
        else: 
            angz=angz
    except Exception as err:
        print(err)

def VelScan(data):
    global angz
    global LINX
    LINX = data.linear.x
    angz = data.angular.z

def main():
    
    rospy.init_node('listener', anonymous=True)

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    rospy.Subscriber("/cmd_vel",Twist, VelScan)
    rospy.Subscriber("/SF", sensor_msgs.msg.Range , SonarFScan)
    rospy.Subscriber("/SL", sensor_msgs.msg.Range , SonarLScan)
    rospy.Subscriber("/SR", sensor_msgs.msg.Range , SonarRScan)

    rate = rospy.Rate(20) # 10hz

    while not rospy.is_shutdown():
        command = Twist()
        command.linear.x = LINX
        command.angular.z = angz
        pub.publish(command)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")
