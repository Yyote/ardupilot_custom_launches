import os

from ament_index_python.packages import get_package_share_directory

import launch_ros.actions as actions

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    ld = LaunchDescription()
    
    
    ld.add_action(actions.Node(
        package="mavsdk_bridge",
        executable="precision_landing_transmitter",
        name="prec_land_transmitter"
    ))
    
    ld.add_action(actions.Node(
        package="coordinate_conversion_py",
        executable="node",
        name="coordinate_conversion_node"
    ))

    ld.add_action(actions.Node(
        package="aruco_precision_landing_ardupilot",
        executable="aruco_infred_landing_node",
        name="aruco_infred_landing_node"
    ))
    
    
    return ld

