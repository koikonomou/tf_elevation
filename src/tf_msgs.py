#!/usr/bin/env python
import rospy
import math
import tf
import numpy 
from grid_map_msgs.msg import GridMap
from tf.msg import tfMessage

tf_broadcaster = None

def init(msg):
    global tf_broadcaster
    global height, position_x, position_y


    height=0
    position_x=0
    position_y=0
    b=False
    index=0

    col_sz=msg.data[0].layout.dim[0].size
    row_sz=msg.data[0].layout.dim[1].size
    res = msg.info.resolution
    p_x = msg.info.pose.position.x
    p_y = msg.info.pose.position.y


#    msg_.info.pose.orientation.x=0
#    msg_.info.pose.orientation.y=0
#    msg_.info.pose.orientation.z=0
#    msg_.info.pose.orientation.w=1.

    i=0
    for k in range (len(msg.layers)):
        if msg.layers[k]=="elevation" :
            i = k
            break
    for j in range (0,numpy.ma.size(msg.data[i].data)):
#            print len(msg_.data)
#            print numpy.ma.size(msg_.data)
#            print numpy.ma.size(msg_.data[i].data)
#            print len(msg_.data[i].data)

        if (numpy.isnan(msg.data[i].data[j])==False) and (numpy.isinf(msg.data[i].data[j])==False):
#               if (b==False):
#                height = msg_.data[i].data[j] #- 3.0 * 2.486
#                    b=True
            if (msg.data[i].data[j] > height):
                height = msg.data[i].data[j]
                index = j
#        if (msg_.data[i].data[j] == height):
    position_y = ((row_sz / 2) * res) - (int(index / row_sz) * res) + p_y
    position_x = ((col_sz / 2) * res) - (int(index % col_sz) * res) + p_x
    tf_broadcaster.sendTransform(
        (position_x , position_y , height),
        (0, 0, 0, 1.0),
        rospy.Time.now(),
        "elev_tf"+str(i),
        "/base_link")



    print (height)
    print (index)
    print (position_x)
    print (position_y)


if __name__=='__main__':
    rospy.init_node('tf_elevation')
    tf_broadcaster = tf.TransformBroadcaster()

    rospy.Subscriber('/elevation_mapping/elevation_map', GridMap, init)
    while not rospy.is_shutdown():
        rospy.spin()
