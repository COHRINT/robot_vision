import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

class Publisher:
    def __init__(self, cameraport, topic='image_topic', publishrate=0):
        self.publishrate = publishrate
        rospy.init_node('image_publisher_node', anonymous=True) # init rosnode
        self.publisher = rospy.Publisher(topic, Image, queue_size=10) # init topic to publish to
        self.bridge = CvBridge() # convert opencv image to ros image msg
        self.cam_feed = cv2.VideoCapture(cameraport) # init device we capture from

    def publish_image(self):
        
        # Read image from camera
        ret, img = self.cam_feed.read()
        # Initialize the OpenCV bridge for converting between OpenCV images and ROS messages
        
        # Convert the OpenCV image to a ROS message
        try:
            image_msg = self.bridge.cv2_to_imgmsg(img, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)
            return -1
        
        # Publish the ROS image message
        self.publisher.publish(image_msg)
        # cv2.imshow("publisher",img) - testing, making sure the image is being recieved by the camera
        # Rerun the publish image method
        if (self.publishrate == 0): # publish images as fast as possible
            rospy.spin()
        else:
            rospy.sleep(self.publishrate)
    
def main():
    image = Publisher(0,publishrate=0.1) # create Feed object
    while True:
        if image.publish_image() == -1: break # read and publish the image
        if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1)==27):
            break
        
        
if __name__ == '__main__':
    main()
