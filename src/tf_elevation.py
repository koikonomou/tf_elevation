#!/usr/bin/env python
import rospy
import math
import tf
import numpy 
from grid_map_msgs.msg import GridMap
from tf2_msgs.msg import TFMessage


def init(msg):
    global tf_broadcaster, pub_elevation
    global height, position_x , position_y


    height=0
    position_x=0
    position_y=0
    tf_broadcaster=None
    new_data=[]
    b=False


    msg_ = msg
    msg_.info.header.frame_id = "/camera_link"
    msg_.info.header.stamp = rospy.Time.now()
    msg_.info.resolution=0.06

    msg_.outer_start_index=0
    msg_.inner_start_index=0
    msg_.info.pose.position.x=0.0
    msg_.info.pose.position.y=0.0
    msg_.info.pose.position.z=0.0

    print len(msg_.data)
    for i in range (0,numpy.ma.size(msg_.data)):
        for j in range (0,numpy.ma.size(msg_.data[i].data)):
            if numpy.isnan(msg_.data[i].data[j])==False:
                if (b == False):
                    height = msg_.data[i].data[j]
                    b = True
                 new_data.append(msg_.data[i].data[j])

                if msg_.data[i].data[j] > height :
                    position_x = j / 72.0 * 0.06 
                    position_y = j % 72.0 * 0.06 


    tf_broadcaster = tf.TransformBroadcaster()
    tf_broadcaster.sendTransform(
    (position_x, position_y , height),
    (0, 0, 0, 1.0),
    rospy.Time.now(),
    "elev_tf"+str(i),
    "/camera_link")



    pub_elevation.publish(msg_)

    print (height)
    print (position_x)
    print (position_y)


if __name__=='__main__':
    rospy.init_node('tf_elevation')
    pub_elevation=rospy.Publisher('/elev', GridMap, queue_size=1)
    rospy.Subscriber('/elevation_mapping/elevation_map_raw', GridMap, init)
    while not rospy.is_shutdown():
        rospy.spin()
