import rclpy
from std_msgs.msg import Float32
from sensor_msgs.msg import Image
import cv_bridge
import cv2 

class ImagePublisher:

    def __init__(self,args=None):

        # Initialize the ROS 2 system
        rclpy.init(args=args)

        self.node = rclpy.create_node('imgpublisher')
        self.publisher = self.node.create_publisher(Image, 'imgmsg', 10)
        self.timer_period = 0.5

        # Create a timer that calls the timer_callback function every timer_period seconds
        self.timer = self.node.create_timer(self.timer_period, lambda: self.timer_callback())

        # define a video capture object 
        self.vid = cv2.VideoCapture(0) 

        #Initalize the cv bridge.
        self.cv_bridge = cv_bridge.CvBridge()

        #Initalize Frame count
        self.framec = 0

    def timer_callback(self, *args):

        # Convert opencv to Image msg
        msg = self.cv_bridge.cv2_to_imgmsg(self.capture_video())

        # Publish the message
        self.publisher.publish(msg)

        # Print a message indicating what is being published
        print('Publishing frame:  "%s"' % self.framec)
        self.framec += 1

    def capture_video(self,*args):
        
        # Capture the video frame 
        # by frame 
        ret, frame = self.vid.read() 
        return frame

def main(args = None):
    # Call the main function if this script is the main module

    imgpublisher = ImagePublisher(args)

    try:
        # Start spinning the ROS 2 node
        rclpy.spin(imgpublisher.node)
    finally:
        # Destroy the node explicitly when done spinning
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        imgpublisher.node.destroy_node()

        # Shutdown the ROS 2 system
        rclpy.shutdown()

        # After the loop release the cap object 
        imgpublisher.vid.release() 


# Entry point to the script
if __name__ == '__main__':
    main()
