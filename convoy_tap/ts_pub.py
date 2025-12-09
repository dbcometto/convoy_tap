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
        self.get_logger().info(f"Initing Tapstrap")

        # ROS publishers
        self.tap_pub = self.create_publisher(UInt8, 'tap_topic', 10)
        self.gesture_pub = self.create_publisher(Int8, 'gesture_topic', 10)

        # # Create asyncio event loop
        # self.loop = asyncio.get_event_loop()
        # self.loop.set_debug(True)

        # # Timer to schedule the async TapSDK coroutine once
        # self.create_timer(0.1, self.async_wrapper)
        # self.tap_task = None  # store the task so it's not garbage collected



        # super().__init__('tapstrap_publisher')
        # self.tap_pub = self.create_publisher(UInt8, 'tap_topic', 10)
        # self.gesture_pub = self.create_publisher(Int8, 'gesture_topic', 10)

        # loop = asyncio.get_event_loop()
        # loop.set_debug(True)
        # loop.run_until_complete(self.run(loop))



        # Create a new asyncio event loop for TapSDK
        self.loop = asyncio.new_event_loop()

        # Start the asyncio loop in a separate thread
        self.thread = threading.Thread(target=self.start_loop, daemon=True)
        self.thread.start()

        # Schedule TapSDK coroutine
        self.tap_task = asyncio.run_coroutine_threadsafe(self.run_tapsdk(), self.loop)

    def start_loop(self):
        """Run the asyncio event loop forever in a separate thread."""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def run_tapsdk(self):
        """TapSDK connection loop with automatic reconnect."""
        # self.get_logger().info(f"async run")
        while rclpy.ok():
            if self.client is None:
                try:
                    self.get_logger().warn("aLIVE")
                    self.client = TapSDK(loop=self.loop)
                    await self.client.run()
                    # Register callbacks
                    await self.client.register_tap_events(self.onTapped)
                    # await self.client.register_air_gesture_events(self.onGesture)
                    await self.client.connection_lost(self.onDisconnected)
                    await self.client.set_input_mode(TapInputMode("controller"))
                except Exception as e:
                    self.get_logger().warn(f"TapSDK connection error: {e}")
                    await asyncio.sleep(2.0)
            else:
                await asyncio.sleep(0.1)





        # while rclpy.ok():
        #     client = None
        #     try:
        #         client = TapSDK(loop=self.loop)
        #         await client.run()
        #         self.get_logger().info(f"Connected: {client.client.is_connected}")

        #         # Register events
        #         await client.register_tap_events(self.onTapped)
        #         # await client.register_air_gesture_events(self.onGesture)
        #         await client.set_input_mode(TapInputMode("controller"))

        #         # Keep alive while connected
        #         while rclpy.ok():
        #             self.get_logger().warn("aLIVE")
        #             if not getattr(client, "client", None) or not client.client.is_connected:
        #                 self.get_logger().warn("TapSDK disconnected, reconnecting...")
        #                 break  # exit inner loop to reconnect
        #             await asyncio.sleep(0.1)


        #     except Exception as e:
        #         self.get_logger().info(f"TapSDK connection error: {e}")

        #     finally:
        #         # Cleanup only if client was partially connected
        #         if client is not None and hasattr(client, "client") and client.client.is_connected:
        #             try:
        #                 await client.client.disconnect()
        #             except Exception:
        #                 pass

        #     # Wait before retrying
        #     await asyncio.sleep(2.0)


        # """Connect to TapSDK and register events, with automatic reconnect."""
        # while rclpy.ok():
        #     try:
        #         client = TapSDK(loop=self.loop)
        #         await client.run()
        #         self.get_logger().info(f"Connected: {client.client.is_connected}")

        #         # Register events
        #         await client.register_tap_events(self.onTapped)
        #         # await client.register_air_gesture_events(self.onGesture)
        #         await client.set_input_mode(TapInputMode("controller"))

        #         # Keep running while connected
        #         while rclpy.ok() and client.client.is_connected:
        #             await asyncio.sleep(0.1)

        #     except Exception as e:
        #         self.get_logger().info(f"TapSDK connection lost: {e}")
        #         await asyncio.sleep(1.0)  # wait before retrying

    def onDisconnected(self, identifier):
        self.get_logger().info(f"Tap Strap {identifier} disconnected, reconnecting...")
        # Cancel current client and allow outer loop to reconnect
        if hasattr(self, "client") and self.client:
            asyncio.create_task(self.client.client.disconnect())
        self.client = None


    # def async_wrapper(self):
    #     """Schedules the TapSDK coroutine in the ROS thread safely."""
    #     if self.tap_task is None:
    #         self.tap_task = asyncio.ensure_future(self.run())


    # async def run(self):
    #     while rclpy.ok():
    #         self.get_logger().info(f"Asyncio Running")
    #         try:
    #             client = TapSDK(loop=self.loop)
    #             await client.run()
    #             self.get_logger().info(f"Connected: {client.client.is_connected}")

    #             # await client.register_air_gesture_events(self.onGesture)
    #             await client.register_tap_events(self.onTapped)
    #             await client.set_input_mode(TapInputMode("controller"))

    #             # Keep running while connected
    #             while rclpy.ok() and client.client.is_connected:
    #                 await asyncio.sleep(0.1)

    #         except Exception as e:
    #             self.get_logger().info(f"TapSDK connection lost: {e}")
    #             await asyncio.sleep(1.0)  # wait before retrying


    # async def run(self, loop):
    #     client = TapSDK(loop=loop)
    #     await client.run()
    #     self.get_logger().info("Connected: {0}".format(client.client.is_connected))

    #     await client.register_air_gesture_events(self.OnGesture)
    #     await client.register_tap_events(self.OnTapped)
    #     #await client.register_raw_data_events(self.OnRawData)
    #     #await client.register_mouse_events(self.OnMoused)
    #     #await client.register_air_gesture_state_events(self.OnMouseModeChange)

    #     print("Set Controller Mode")
    #     await client.set_input_mode(TapInputMode("controller"))
    #     #print("Set auto Mode")
    #     #await client.set_input_type(InputType.AUTO)
    #     await asyncio.sleep(1000000)


    # def onMouseModeChange(self, identifier, mouse_mode):
    #     print(str(identifier) + " changed to mode " + str(mouse_mode))


    def onTapped(self, identifier, tapcode):
        print(str(identifier) + " tapped " + str(tapcode))
        msg = UInt8()
        msg.data = tapcode
        self.tap_pub.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')


    # def onGesture(self, identifier, gesture):
    #     print(str(identifier) + " gesture " + str(AirGestures(gesture)))
    #     msg = Int8()
    #     msg.data = gesture
    #     self.gesture_pub.publish(msg)
    #     self.get_logger().info(f'Publishing: "{msg.data}"')


    #def OnMoused(self, identifier, vx, vy, isMouse):
        #print(str(identifier) + " mouse movement: %d, %d, %d" % (vx, vy, isMouse))


    #def OnRawData(self, identifier, packets):
        #for m in packets:
            #print(f"{m['type']}, {time.time()}, {m['payload']}")

    #tap
    
    # async def tap_event(identifier, tapcode):
    #     self.get_logger().info(f"{identifier} - Tapped {tapcode}")
    #     msg = UInt8()
    #     msg.data = tapcode
    #     self.tap_pub.publish(msg)
    #     self.get_logger().info(f'Publishing: "{msg.data}"')

    # #gesture
    # async def gesture_event(identifier, gesture):
    #     gesture_name = AirGestures(gesture).name  # Use AirGestures to get the gesture name
    #     self.get_logger().info(f"{identifier} - Gesture: {gesture_name}")
    #     msg = Int8()
    #     msg.data = gesture
    #     self.gesture_pub.publish(msg)
    #     self.get_logger().info(f'Publishing: "{msg.data}"')
    



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



