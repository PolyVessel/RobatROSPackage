#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
from drivers import GPS, GPSNoSignal
from drivers.util import TimeoutException

def get_gps_data(gps):
    try:
        return gps.poll_sensor()

    # Critical, Expected Errors
    except TimeoutException as e:
        rospy.logfatal_throttle(180, "GPS Module Not Connected")
    except GPSNoSignal as e:
        rospy.log_throttle(180, "No GPS Signal")

    # More serious errors, that would not be expected
    except ValueError as e:
        rospy.logfatal_throttle_identical(120, "Value Error thrown by GPS node! Details: " + str(e))
    except IOError as e:
        rospy.logfatal_throttle_identical(120, "IO Error thrown by GPS node! Details: " + str(e))

def gps_location_publisher():
    pos_lat = rospy.Publisher('GPS_position_lat', Float64, queue_size=5)
    pos_lon = rospy.Publisher('GPS_position_lon',Float64, queue_size=5)
    vel_pub = rospy.Publisher('GPS_velocity', Float64, queue_size=5)
    rospy.init_node('gps')
    rate = rospy.Rate(0.5) # 0.5hz
    gps = GPS()
    rospy.loginfo("GPS Initialized")
    
    while not rospy.is_shutdown():
        data = get_gps_data(gps)
        if data is not None:
            pos_lon.publish(data.lon)
            pos_lat.publish(data.lat)
            vel_pub.publish(data.gSpeed)
            rospy.loginfo("Lon: {}, Lat: {}".format(data.lon, data.lat))

        rate.sleep()

if __name__ == '__main__':
    try:
        gps_location_publisher()
    except rospy.ROSInterruptException:
        pass

