from launch import LaunchDescription
import launch_ros.actions as actions

def generate_launch_description():
    ld = LaunchDescription()

    ld.add_action(actions.Node(
        package="mavsdk_bridge",
        executable="precision_landing_transmitter",
        name="precision_landing_transmitter"
    ))
    
    ld.add_action(actions.Node(
        package="coordinate_conversion_py",
        executable="node",
        name="node"
    ))

    # ld.add_action(actions.Node(
    #     package="aruco_precision_landing_ardupilot",
    #     executable="node",
    #     name="node"
    # ))

    return ld