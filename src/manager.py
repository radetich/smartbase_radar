import rospy
from track import *
#import target

from smartbase_radar.msg import RadarTargetArray


# callback
def callback(data):
    array = []
    rospy.loginfo(len(data))
    for target in data.targets:
        print(target)
    #   append(Track(target. , t.))
    
    target.manager(array)


# listener for radar data   
def listener(topic):
    rospy.Subscriber(topic, RadarTargetArray, callback)


if __name__ == '__init__':
    rospy.init_node('listener', anonymous = True)
    
    # got topic from rosBAG -- this is the raw can bus data

    topics = ["/srr2_front/targets_left", "/srr2_front/targets_right"]

    for topic in topics:
        listener(topic)

    # keeps python moving until data is used
    rospy.spin()