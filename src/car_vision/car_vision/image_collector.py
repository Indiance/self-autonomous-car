#!/usr/bin/env python3
import os
import time
from datetime import datetime

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class ImageCollector(Node):
    def __init__(self):
        super().__init__('image_collector')

        self.declare_parameter('topic', 'camera/image_raw')
        self.declare_parameter('output_dir', os.path.expanduser(
            '~/Desktop/self_autonomous_car/data/captures'))
        self.declare_parameter('save_rate', 1.0)
        self.declare_parameter('image_format', 'jpg')
        self.declare_parameter('session_name', '')

        topic = self.get_parameter('topic').value
        base_dir = os.path.expanduser(self.get_parameter('output_dir').value)
        self.save_rate = float(self.get_parameter('save_rate').value)
        self.image_format = self.get_parameter('image_format').value.lstrip('.')
        session_name = self.get_parameter('session_name').value

        session_name = session_name or datetime.now().strftime('session_%Y%m%d_%H%M%S')
        self.session_dir = os.path.join(base_dir, session_name)
        os.makedirs(self.session_dir, exist_ok=True)

        self.bridge = CvBridge()
        self.min_period = 1.0 / self.save_rate if self.save_rate > 0 else 0.0
        self.last_save_time = 0.0
        self.frame_count = 0

        self.subscription = self.create_subscription(
            Image, topic, self.listener_callback, 10)

        self.get_logger().info(
            f'Saving frames from "{topic}" to "{self.session_dir}" '
            f'at up to {self.save_rate} fps')

    def listener_callback(self, msg):
        now = time.monotonic()
        if now - self.last_save_time < self.min_period:
            return
        self.last_save_time = now

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        filename = os.path.join(
            self.session_dir, f'frame_{self.frame_count:06d}.{self.image_format}')
        cv2.imwrite(filename, frame)
        self.frame_count += 1

        if self.frame_count % 20 == 0:
            self.get_logger().info(f'Saved {self.frame_count} frames so far')


def main(args=None):
    rclpy.init(args=args)
    node = ImageCollector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.get_logger().info(f'Saved {node.frame_count} frames total to {node.session_dir}')
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
