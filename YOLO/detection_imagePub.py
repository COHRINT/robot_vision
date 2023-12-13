from cProfile import label

# The following script imports the ObjectDetection class
from imageai.Detection import ObjectDetection

# Import the message publisher function
#from objectInfomessagePublisher import messagePublisher2 
from image_messagePublisher import publish_image

import cv2
# The script below creates an object of the object detection class.
obj_detect = ObjectDetection()

# The next step is to set the model type for object detection. Since we’ll be using the YOLO algorithm, you need to call the setModelTypeAsYOLOv3() method as shown in the script below:
obj_detect.setModelTypeAsYOLOv3()

# The next step is to load the actual Yolo model. The Yolo model the imageai library uses for object detection is available at the following Github Link: https://bit.ly/2UqlRGD
# To load the model, first you need to call the setModelPath() method from your ObjectDetection class object and pass it the path where you downloaded the yolo.h5 model. 
# Next, you need to call the loadModel() method to actually load the model. Look at the following script for reference:
obj_detect.setModelPath(r"/home/walle/COHRINT/yolo.h5")
obj_detect.loadModel()

# The next step is to capture your webcam stream. To do so, execute the script below:
cam_feed = cv2.VideoCapture(0)

# Next, you need to define height and width for the frame that will display the detected objects from your live feed. 
# Execute the following script to do so, recognizing you can change the integer values near the end to match your desired dimensions:
cam_feed.set(cv2.CAP_PROP_FRAME_WIDTH, 650)
cam_feed.set(cv2.CAP_PROP_FRAME_HEIGHT, 750)

#obj2 = ImagePublisher()
#obj1 = messagePublisher2()

while True:    
    # Reads the next frame captured by the camera
    ret, img = cam_feed.read()   
    
    # This function outputs the annote_image and a dictionnary of the detected object containing its name, percentage probability, and bounding boxes dimensions
    annotated_image, preds = obj_detect.detectObjectsFromImage(input_image=img,
                    input_type="array",
                      output_type="array",
                      display_percentage_probability=False,
                      display_object_name=True)
    
    # Publish the message (detected object dictionnary)
    #obj1.message_publisher2(preds)
    #obj2.publish_image(annotated_image)
    publish_image(annotated_image)

    # Display the current frame containing our detected objects
    #cv2.imshow("", annotated_image)
    # matplotlib.imshow(raw image)
    # matplotlib.patches.Rectangle(xy,....)
    # text  box


    # To stop the program, press "q" or "ESC"
    if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1)==27):
        break
    

cam_feed.release()
cv2.destroyAllWindows()