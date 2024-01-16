import rclpy
from sensor_msgs.msg import Image
import cv_bridge
import cv2 
import numpy as np

class ImageSubscriber:

    def __init__(self,args=None):

        # Initialize the ROS 2 system
        rclpy.init(args=args)

        self.node = rclpy.create_node('imgsubscriber')
        self.subscriber = self.node.create_subscription(Image, 'imgmsg', self.listner_callback, 10)

        #Initalize the cv bridge.
        self.cv_bridge = cv_bridge.CvBridge()

        #Initalize Frame count
        self.framec = 0

        #Initalixe variables for canny detection.
        self.t_lower = 50 # Lower Threshold
        self.t_upper = 150 # Upper Threshold


    def listner_callback(self, msg, *args):

        img = self.cv_bridge.imgmsg_to_cv2(msg)
        canny_img = self.canny_image(img)

        cv2.imshow('Orginal And Canny Image', self.stack_images(img,canny_img))
        cv2.waitKey(1)

        # Print a message indicating what is being received.
        print('Receiving frame:  "%s"' % self.framec)
        self.framec += 1


    def canny_image(self,img,*args):
        return cv2.Canny(img,self.t_lower,self.t_upper)    

    def stack_images(self,img1,img2,*args):


        # Convert the canny image into 3-d image(RGB) otherwise it can't be stacked with original image.
        two_d_image = img2

        # Create a 3D array with three channels (R, G, B)
        height, width = two_d_image.shape
        channels = 3
        three_d_image = np.zeros((height, width, channels), dtype=np.uint8)

        # Set the RGB values based on the 2D array
        three_d_image[:, :, 0] = two_d_image  # Red channel
        three_d_image[:, :, 1] = two_d_image  # Green channel
        three_d_image[:, :, 2] = two_d_image  # Blue channel

        return cv2.hconcat([img1,three_d_image])

def main(args = None):

    # Call the main function if this script is the main module

    imgsubscriber = ImageSubscriber(args)

    try:
        # Start spinning the ROS 2 node
        rclpy.spin(imgsubscriber.node)
    finally:
        # Destroy the node explicitly when done spinning
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        imgsubscriber.node.destroy_node()

        # Shutdown the ROS 2 system
        rclpy.shutdown()

        # Destroy all cv2 windows.
        cv2.destroyAllWindows() 




# Entry point to the script
if __name__ == '__main__':
    main()