#!/usr/bin/env python
import rospy
import math
from grid_map_msgs.msg import GridMap


elevationmap_publisher = None

def elevationmap_callback(msg):
    global elevationmap_publisher

    minheight=0
    maxheight=0
    b = False
    new_data= []
    for i in range(0, len(msg.data)):
        for j in range(0,len(msg.data[i].data)):
            if math.isnan(msg.data[i].data[j]) == False :
                if(b == False):
                    minheight = msg.data[i].data[j]
                    maxheight = msg.data[i].data[j]
                    b = True
#                print (msg.data[i].data[j] )
                new_data.append(msg.data[i].data[j])
                if msg.data[i].data[i] < minheight :
                    minheight =msg.data[i].data[j]
                if msg.data[i].data[j] > maxheight :
                    maxheight = msg.data[i].data[j]
#    print(new_data)
    elevationmap_publisher.publish(msg)
    print (minheight)
    print (maxheight)




if __name__ == '__main__':
    rospy.init_node('elevation_map')
    rospy.Subscriber('/elevation_mapping/elevation_map', GridMap, elevationmap_callback)
    elevationmap_publisher = rospy.Publisher('elevation', GridMap, queue_size=1)
    rospy.spin()