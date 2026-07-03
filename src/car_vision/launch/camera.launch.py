from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('sensor_id', default_value='0'),
        DeclareLaunchArgument('width', default_value='1280'),
        DeclareLaunchArgument('height', default_value='720'),
        DeclareLaunchArgument('framerate', default_value='30'),
        DeclareLaunchArgument('flip_method', default_value='0'),
        DeclareLaunchArgument('view', default_value='false',
                               description='Also launch the local cv2 image viewer window'),
        DeclareLaunchArgument('collect', default_value='false',
                               description='Also launch the dataset image collector node'),
        DeclareLaunchArgument('save_rate', default_value='1.0',
                               description='Frames per second saved by the image collector'),

        Node(
            package='car_vision',
            executable='csi_camera_publisher',
            name='csi_camera_publisher',
            output='screen',
            parameters=[{
                'sensor_id': LaunchConfiguration('sensor_id'),
                'width': LaunchConfiguration('width'),
                'height': LaunchConfiguration('height'),
                'framerate': LaunchConfiguration('framerate'),
                'flip_method': LaunchConfiguration('flip_method'),
            }],
        ),

        Node(
            package='car_vision',
            executable='image_viewer',
            name='image_viewer',
            output='screen',
            condition=IfCondition(LaunchConfiguration('view')),
        ),

        Node(
            package='car_vision',
            executable='image_collector',
            name='image_collector',
            output='screen',
            parameters=[{
                'save_rate': LaunchConfiguration('save_rate'),
            }],
            condition=IfCondition(LaunchConfiguration('collect')),
        ),
    ])
