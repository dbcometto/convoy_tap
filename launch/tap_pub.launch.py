import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction


def generate_launch_description():
    
    workspace = os.path.expanduser("~/workspace/cvy_ws")
    tap_python = f"{workspace}/venvs/tap_env/bin/python3"
    
    ros_pythonpath = ":".join([
        f"{workspace}/install/convoy_tap/lib/python3.10/site-packages",
        f"{workspace}/install/convoy_interfaces/lib/python3.10/site-packages",
        "/opt/ros/humble/lib/python3.10/site-packages",
        "/opt/ros/humble/local/lib/python3.10/dist-packages",
    ])
    
    ts_node = ExecuteProcess(
        cmd=[
            tap_python,
            f"{workspace}/install/convoy_tap/lib/python3.10/site-packages/convoy_tap/ts_pub.py"
        ],
        name="ts_pub",
        output="screen",
        additional_env={"PYTHONPATH": ros_pythonpath},
    )
    
    delayed_node = TimerAction(
        period=3.0,
        actions=[ts_node]
    )

    return LaunchDescription([
        delayed_node
    ])