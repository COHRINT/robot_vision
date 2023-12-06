import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

class Feed:
    def __init__(self, cameraport, topic='image_topic', publishrate=0):
        self.publishrate = publishrate
        self.camera = cameraport
        rospy.init_node('image_publisher_node', anonymous=True)
        self.publisher = rospy.Publisher(topic, Image, queue_size=10)
        self.bridge = CvBridge()
        self.counter = 0
        self.cam_feed = cv2.VideoCapture(self.camera)

    def publish_image(self, topic='image_topic'):
        
        
        ret, img = self.cam_feed.read()
        # Initialize the OpenCV bridge for converting between OpenCV images and ROS messages
        self.counter = self.counter + 1
        print(self.counter,':\n',img)
        
        # Convert the OpenCV image to a ROS message
        try:
            image_msg = self.bridge.cv2_to_imgmsg(img, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)
            return -1
        
        # Publish the ROS image message
        self.publisher.publish(image_msg)
        # cv2.imshow("publisher",img)
        
        if (self.publishrate == 0):
            rospy.spin()
        else:
            rospy.sleep(0.1)
    
def main():
    image = Feed(0,publishrate=0.5)
    while True:
        if image.publish_image() == -1: break
        if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1)==27):
            break
        
        
if __name__ == '__main__':
    main()
