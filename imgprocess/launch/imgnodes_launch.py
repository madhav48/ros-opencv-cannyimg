from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='imgprocess',
            executable='imgpublisher',
        ),
        Node(
            package='imgprocess',
            executable='imgsubscriber',
        ),
    ])