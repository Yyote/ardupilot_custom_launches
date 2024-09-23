import os
from getpass import getuser
from ament_index_python.packages import get_package_share_directory

import launch_ros.actions as actions

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource


def generate_launch_description():
    user = getuser()

    print(f'LAUNCH: \n\tCurrent working directory: {os.getcwd()}')

    ld = LaunchDescription()
    
    ld.add_action(actions.Node(
        package="mavsdk_bridge",
        executable="precision_landing_transmitter",
        name="prec_land_transmitter",
        emulate_tty=True, output='screen',
        namespace="wired_uav",
        parameters=[
            {"username": user},
            # {"pld_kp": 4.8}, # Ku 7.75, Tu 0.623
            # {"pld_kd": 5.362},
            # {"pld_ki": 0.5},
            {"pld_kp": 2.2}, # Ku 7.75, Tu 0.623
            {"pld_kd": 0.55},
            {"pld_ki": 0.0025},
            {"pld_max_spd": 0.5},
            {"pld_acc_radius_deg": 2.0},
            {"pld_fin_appr_alt": 1.5}
        ]
    ))
    
    ld.add_action(actions.Node(
        package="coordinate_conversion_py",
        executable="node",
        name="coordinate_conversion_node",
        namespace="wired_uav"
    ))

    ld.add_action(actions.Node(
        package="aruco_precision_landing_ardupilot",
        executable="aruco_infred_landing_node",
        name="aruco_infred_landing_node",
        namespace="wired_uav"
    ))
    
    ld.add_action(actions.Node(
        package="video_capture_ros2",
        executable="video_capture_node",
        name="video_capture_node",
#        namespace="wired_uav"
        parameters=[
            {'video_topic_name': '/wired_uav/camera/detected_markers'},
            {'path_to_video_dir': f'/home/{user}/'},
            {'framerate': '90'}
        ]
    ))
    
    mavproxy = None

    if user == 'firefly' or user == 'panda':
        mavproxy = ExecuteProcess(
            cmd=[[
                'mavproxy.py --out 127.0.0.1:14551 --out 127.0.0.1:14552 --master /dev/ttyS7,921600',
            ]],
            shell=True
        )
    else:
        mavproxy = ExecuteProcess(
            cmd=[[
                'mavproxy.py --out 127.0.0.1:14551 --out 127.0.0.1:14552 --master udp:127.0.0.1:14550',
            ]],
            shell=True
        )

    ld.add_action(mavproxy)

    args = None

    if user == 'firefly' or user == 'panda':
        args = {
            'fcu_url' : 'udp://:14552@127.0.0.1:14552',
            # 'fcu_url' : '/dev/ttyUSB0:115200',
            'tgt_system' : "5"
        }.items()
    else:
        args = {
            'fcu_url' : 'udp://:14553@127.0.0.1:14553',
            # 'fcu_url' : '/dev/ttyUSB0:115200',
            'tgt_system' : "1",
        }.items()

    ld.add_action(IncludeLaunchDescription(
        XMLLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mavros'), 'launch/'),
            'px4.launch']), launch_arguments=args
    ))
    
    ld.add_action(GroupAction([
        actions.PushRosNamespace("wired_uav"),
        IncludeLaunchDescription(XMLLaunchDescriptionSource([os.path.join(get_package_share_directory('mavros'), 'launch/'), 'px4.launch']), launch_arguments=args),
        ]))
    
    
    return ld

