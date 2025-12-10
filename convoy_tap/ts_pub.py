from tapsdk import TapSDK, TapInputMode
from tapsdk.models import AirGestures
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8, Int8 #tap is an unsigned 8 bit int, for example,20 = 10100 = thumb and middle finger tapped, Int8 for gesture
import asyncio
import threading

# tap_device = TapSDK()

class TSPublisher(Node):

    def __init__(self):
        super().__init__('tapstrap_publisher')
        self.get_logger().info(f"Initializing Tapstrap")

        # ROS publishers
        self.tap_pub = self.create_publisher(UInt8, 'tap_topic', 10)
        self.gesture_pub = self.create_publisher(Int8, 'gesture_topic', 10)

        # Bluetooth Thread
        self.client = None
        self.loop = asyncio.new_event_loop()

        self.thread = threading.Thread(target=self.start_loop, daemon=True)
        self.thread.start()

        self.tap_task = asyncio.run_coroutine_threadsafe(self.run_tapsdk(), self.loop)



    def start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()



    async def run_tapsdk(self):
        try:
            # self.get_logger().info(f"async run")
            while rclpy.ok():

                if self.client is None: # If no client, try to connect
                    try:
                        self.get_logger().info("Attempting to connect to tapstrap")

                        try:
                            self.client = TapSDK(loop=self.loop)
                        except Exception as e:
                            self.client = None
                            self.get_logger().warn(f"TapSDK formation error") #: {e}
                            await asyncio.sleep(4.0)

                        # self.get_logger().info("1a")
                        await self.client.run()
                        # self.get_logger().info(f"Connected: {self.client.client.is_connected()}")

                        while not getattr(self.client, "client", None) and not await self.client.client.is_connected():
                            # self.get_logger().info("waiting")
                            await asyncio.sleep(0.5)

                        # await self.client.register_connection_events(self.onConnected)
                        # self.get_logger().info("3a")
                        await self.client.register_tap_events(self.onTapped)
                        # await self.client.register_air_gesture_events(self.onGesture)
                        # await self.client.register_disconnection_events(self.onDisconnected)
                        await self.client.set_input_mode(TapInputMode("controller"))

                        self.get_logger().info(f"Tapstrap is ready for use")

                        

                    except Exception as e:
                        self.get_logger().warn(f"TapSDK connection error ") #: {e}
                        self.client = None
                        await asyncio.sleep(4.0)


                else: # Client exists
                    if getattr(self.client, "client", None): # Check if still connected
                        try:
                            connected = await self.client.client.is_connected()
                        except Exception as e:
                            self.get_logger().warn(f"Error checking connection") #: {e}
                            connected = False

                        if not connected: # If not connected, mark for reconnection
                            self.get_logger().warn("Tap Strap disconnected, will reconnect")
                            # Cancel background run task if you stored it
                            if hasattr(self, "_run_task") and self._run_task:
                                self._run_task.cancel()
                            self.client = None
                            await asyncio.sleep(4.0)

                        else: # If connected, proceed as normal
                            # self.get_logger().info("Tap Strap is connected")
                            pass

                    else: # Check if client broken and reconnect
                        self.get_logger().warn("TapSDK exists but client is None, will reconnect")
                        self.client = None
                        await asyncio.sleep(4.0)

                    await asyncio.sleep(0.1)

        except Exception as e:
            self.get_logger().warn(f"Bluetooth Thread Crash: {e}")


    # def onMouseModeChange(self, identifier, mouse_mode):
    #     print(str(identifier) + " changed to mode " + str(mouse_mode))


    def onTapped(self, identifier, tapcode):
        # print(str(identifier) + " tapped " + str(tapcode))
        msg = UInt8()
        msg.data = tapcode
        self.tap_pub.publish(msg)
        self.get_logger().info(f'Tapstrap: "{msg.data}"')


    # def onGesture(self, identifier, gesture):
    #     print(str(identifier) + " gesture " + str(AirGestures(gesture)))
    #     msg = Int8()
    #     msg.data = gesture
    #     self.gesture_pub.publish(msg)
    #     self.get_logger().info(f'Publishing: "{msg.data}"')


    # def OnMoused(self, identifier, vx, vy, isMouse):
    #     print(str(identifier) + " mouse movement: %d, %d, %d" % (vx, vy, isMouse))


    # def OnRawData(self, identifier, packets):
    #     for m in packets:
    #         print(f"{m['type']}, {time.time()}, {m['payload']}")
    



def main():
    rclpy.init()

    node = TSPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        if rclpy.ok():
            node.get_logger().info("Shutting down")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()



