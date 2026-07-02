#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class ImageViewer(Node):
    def __init__(self):
        super().__init__('image_viewer')
        self.declare_parameter('topic', 'camera/image_raw')
        topic = self.get_parameter('topic').value

        self.bridge = CvBridge()
        self.window_name = 'CSI Camera'
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

        self.subscription = self.create_subscription(
            Image, topic, self.listener_callback, 10)
        self.get_logger().info(f'Subscribed to "{topic}". Press q in the image window to quit.')

    def listener_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        cv2.imshow(self.window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.get_logger().info('Quit key pressed, shutting down.')
            rclpy.shutdown()

    def destroy_node(self):
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ImageViewer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()
