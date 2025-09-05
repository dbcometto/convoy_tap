from tapsdk import TapSDK, TapInputMode
from tapsdk.models import AirGestures
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8, Int8 #tap is an unsigned 8 bit int, for example,20 = 10100 = thumb and middle finger tapped, Int8 for gesture
import asyncio

tap_device = TapSDK()

class TSPublisher(Node):

    def __init__(self):
        super().__init__('tapstrap_publisher')
        self.tap_pub = self.create_publisher(UInt8, 'tap_topic', 10)
        self.gesture_pub = self.create_publisher(Int8, 'gesture_topic', 10)

        loop = asyncio.get_event_loop()
        loop.set_debug(True)
        loop.run_until_complete(self.run(loop))

    async def run(self, loop):
        client = TapSDK(loop=loop)
        await client.run()
        self.get_logger().info("Connected: {0}".format(client.client.is_connected))

        await client.register_air_gesture_events(self.OnGesture)
        await client.register_tap_events(self.OnTapped)
        #await client.register_raw_data_events(self.OnRawData)
        #await client.register_mouse_events(self.OnMoused)
        #await client.register_air_gesture_state_events(self.OnMouseModeChange)

        print("Set Controller Mode")
        await client.set_input_mode(TapInputMode("controller"))
        #print("Set auto Mode")
        #await client.set_input_type(InputType.AUTO)
        await asyncio.sleep(1000000)


    def OnMouseModeChange(self, identifier, mouse_mode):
        print(str(identifier) + " changed to mode " + str(mouse_mode))


    def OnTapped(self, identifier, tapcode):
        print(str(identifier) + " tapped " + str(tapcode))
        msg = UInt8()
        msg.data = tapcode
        self.tap_pub.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')


    def OnGesture(self, identifier, gesture):
        print(str(identifier) + " gesture " + str(AirGestures(gesture)))
        msg = Int8()
        msg.data = gesture
        self.gesture_pub.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')


    #def OnMoused(self, identifier, vx, vy, isMouse):
        #print(str(identifier) + " mouse movement: %d, %d, %d" % (vx, vy, isMouse))


    #def OnRawData(self, identifier, packets):
        #for m in packets:
            #print(f"{m['type']}, {time.time()}, {m['payload']}")

    #tap
    '''
    async def tap_event(identifier, tapcode):
        self.get_logger().info(f"{identifier} - Tapped {tapcode}")
        msg = UInt8()
        msg.data = tapcode
        self.tap_pub.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')

    #gesture
    async def gesture_event(identifier, gesture):
        gesture_name = AirGestures(gesture).name  # Use AirGestures to get the gesture name
        self.get_logger().info(f"{identifier} - Gesture: {gesture_name}")
        msg = Int8()
        msg.data = gesture
        self.gesture_pub.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
    '''



def main():
    rclpy.init()

    ts_pub = TSPublisher()

    rclpy.spin(ts_pub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    ts_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()



