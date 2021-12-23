#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32

TOPIC_NAME = "yaw_kalman_filter"
TOPIC_NAME_PUBLISHER = "yaw_kalman_filter_publisher"


kalman_gain = 0
current_state = 0
uncertainty = 10
predicted_state = 0
predicted_uncertainty = 0
sensor_variance = 2
process_variance = 2


def kalman_filter(measurement):
    global kalman_gain
    global current_state
    global uncertainty
    global predicted_state
    global predicted_uncertainty

    predicted_state = current_state
    predicted_uncertainty = uncertainty + process_variance

    kalman_gain = predicted_uncertainty / (predicted_uncertainty + sensor_variance)
    current_state = predicted_state + kalman_gain * (measurement.data - predicted_state)
    uncertainty = (1 - kalman_gain) * predicted_uncertainty

    rospy.loginfo(current_state)
    pub.publish(current_state)


def listener():
    rospy.Subscriber(TOPIC_NAME, Float32, kalman_filter)
    rospy.loginfo(current_state)
    rospy.spin()
    
        
if __name__ == "__main__":
    pub = rospy.Publisher(TOPIC_NAME_PUBLISHER, Float32, queue_size=10)
    rospy.init_node(TOPIC_NAME + '_listener')   
    listener()
