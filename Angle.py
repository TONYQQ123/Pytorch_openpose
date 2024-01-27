from xml.etree.ElementTree import tostring
import numpy as np
import cv2
import math

def Angle(x1,y1,x2,y2,x3,y3):
    A=(x2-x1,y2-y1)
    B=(x3-x1,y3-y1)

    dot_product=np.dot(A,B)
    dis_A=math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
    dis_B=math.sqrt((x3-x1)*(x3-x1)+(y3-y1)*(y3-y1))
    radians=math.acos(dot_product/(dis_A*dis_B))
    degree=math.degrees(radians)
    return degree


def Caculate_angle(candidate):
    arm_left=0.0
    arm_right=0.0
    knee_left=0.0
    knee_right=0.0
    neck=0.0

    neck=Angle(candidate[1][0],candidate[1][1],candidate[0][0],candidate[0][1],candidate[1][0],0.0)
    arm_right=Angle(candidate[3][0],candidate[3][1],candidate[2][0],candidate[2][1],candidate[4][0],candidate[4][1])
    arm_left=Angle(candidate[6][0],candidate[6][1],candidate[5][0],candidate[5][1],candidate[7][0],candidate[7][1])
    knee_right=Angle(candidate[9][0],candidate[9][1],candidate[8][0],candidate[8][1],candidate[10][0],candidate[10][1])
    knee_left=Angle(candidate[12][0],candidate[12][1],candidate[11][0],candidate[11][1],candidate[13][0],candidate[13][1])
    result=(neck,arm_left,arm_right,knee_left,knee_right)
    with open('Angle.txt','w') as file:
        file.write('neck: '+str(neck)+'\n')
        file.write('Arm_left: '+str(arm_left)+'\n')
        file.write('Arm_right: '+str(arm_right)+'\n')
        file.write('knee_right: '+str(knee_right)+'\n')
        file.write('knee_right: '+str(knee_right)+'\n')

    return result

