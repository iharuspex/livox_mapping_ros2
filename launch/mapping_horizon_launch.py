import os

from ament_index_python import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node

map_file_path=''
filter_parameter_corner=0.2
filter_parameter_surf=0.4

laser_mapping_parameters=[
  { "map_file_path": map_file_path },
  { "filter_parameter_corner": filter_parameter_corner },
  { "filter_parameter_surf": filter_parameter_surf }
]

rviz_config_path = os.path.join(
  get_package_share_directory('livox_mapping_ros2'), 'rviz_cfg/loam_livox.rviz'
)


def generate_launch_description():
  scan_registration_horizon = Node(
    package='livox_mapping_ros2',
    executable='loam_scanRegistration_horizon',
    output='screen',
    name='scanRegistration_horizon',
  )

  laser_mapping = Node(
    package='livox_mapping_ros2',
    executable='loam_laserMapping',
    name='laserMapping',
    output='screen',
    parameters=laser_mapping_parameters
  )

  livox_repub = Node(
    package='livox_mapping_ros2',
    executable='livox_repub',
    name='livox_repub',
    output='screen',
    remappings=[
      ('/livox/lidar', '/livox/lidar')
    ]
  )

  livox_rviz = Node(
      package='rviz2',
      executable='rviz2',
      name='rviz',
      output='screen',
      arguments=['--display-config', rviz_config_path]
  )

  return LaunchDescription([
    scan_registration_horizon,
    laser_mapping,
    livox_repub,
    livox_rviz,
  ])