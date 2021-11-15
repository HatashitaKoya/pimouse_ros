#!/usr/bin/env python

import tty, termios, time
import sys, select, os
import rospy

settings = termios.tcgetattr(sys.stdin)

def GetKey():
    key = ""
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__ == '__main__':
    rospy.init_node('vel_publisher')
    afile = "/dev/rtmotoren0"
    ofile = "/dev/rtmotoren0"
    lfile = "/dev/rtmotor_raw_l0"
    rfile = "/dev/rtmotor_raw_r0"
    bfile = "/dev/rtbuzzer0"
    rate = rospy.Rate(10)
    print("i: ON, o: OFF, w: GO, s: BACK, a: LEFT, d: RIGHT, b: buzzer >")
    try:
        while not rospy.is_shutdown():
            key = GetKey()
            if(key=="i"):
                with open(afile, "i") as af:
                    af.write(str(1)+'\n')
                print("ON")
            if(key=="o"):
                with open(ofile, "o") as of:
                    of.write(str(0)+'\n')
                print("OFF")
            if(key=="w"):
                with open(lfile, "w") as lf, open(rfile, "w") as rf:
                    lf.write(str(990)+'\n')
                    rf.write(str(990)+'\n')
                print("GO")
            if(key=="s"):
                with open(lfile, "w") as lf, open(rfile, "w") as rf:
                    lf.write(str(-990)+'\n')
                    rf.write(str(-990)+'\n')
                print("BACK")
            if(key=="a"):
                with open(lfile, "w") as lf, open(rfile, "w") as rf:
                    lf.write(str(-409)+'\n')
                    rf.write(str(409)+'\n')
                print("LEFT")
            if(key=="d"):
                with open(lfile, "w") as lf, open(rfile, "w") as rf:
                    lf.write(str(409)+'\n')
                    rf.write(str(-409)+'\n')
                print("RIGHT")
            if(key=="b"):
                with open(bfile, "b") as bf:
                    bf.write(str(400)+'\n')
                print("ON")
            if(key==""):
                with open(lfile, "w") as lf, open(rfile, "w") as rf:
                    lf.write(str(0)+'\n')
                    rf.write(str(0)+'\n')
            else:
                if (key == '\x03'):
                    break
    except:
        pass
    rate.sleep()
