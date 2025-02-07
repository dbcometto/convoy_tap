import rclpy
from rclpy.node import Node

from std_msgs.msg import UInt8, Int8
from ackermann_msgs.msg import AckermannDriveStamped

class ConvoySub(Node):

    def __init__(self):
        super().__init__('convoy_subscriber')
        self.receiving = False #by default, we dont accept commands

        self.tap_sub = self.create_subscription(
            UInt8,
            'tap_topic',
            self.tap_callback,
            10)

        self.gesture_sub = self.create_subscription(
            Int8,
            'gesture_topic',
            self.gesture_callback,
            10)

        self.drive_pub = self.create_publisher(AckermannDriveStamped, '/veh_1/drive', 10)


        self.tap_sub  # prevent unused variable warning
        self.gesture_sub

    def tap_callback(self, msg):
        if msg.data == 1:
            self.receiving = not self.receiving

        if self.receiving: 
            self.get_logger().info(f'received tap: "{msg.data}"')

            if msg.data == 2:
                drive_msg = AckermannDriveStamped()  # ✅ Correct class instantiation
                drive_msg.header.stamp = self.get_clock().now().to_msg()  # ✅ Proper timestamp
                #drive_msg.header.frame_id = "base_link"  # ✅ Set frame_id if needed

                drive_msg.drive.speed = 1.0  # ✅ Correctly assign a new AckermannDrive instance

                self.drive_pub.publish(drive_msg)  # ✅ Publish correctly
             

    def gesture_callback(self, msg):
        self.get_logger().info(f'received gesture: "{msg.data}"')
        #do something!!
        if msg.data == 2: #one finger up, example for allowing/not allowing commands
            self.receiving = not self.receiving



def main():
    rclpy.init()

    convoy_sub = ConvoySub()

    rclpy.spin(convoy_sub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
