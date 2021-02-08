## Demo Pepper
This is the package contains a quickstart file to start running pepper with ROS.
To run this package, make sure all Pepper ROS components and their dependencies are installed for more information check the wiki.

- https://github.com/ros-naoqi/naoqi_driver (Publishes sensor and actuator data) 
- https://github.com/ros-naoqi/naoqi_bridge (Python version of driver) 
- https://github.com/ros-naoqi/pepper_dcm_robot (Robot controller) 
- https://github.com/ros-naoqi/pepper_moveit_config (Pepper moveit config) 
- https://github.com/ros-naoqi/pepper_robot (URDF + Model) 
- https://github.com/ros-naoqi/pepper_virtual (Pepper gazebo simulation) 

## Quick Launch
```
roslaunch demo_pepper moveit_planner.launch robot_ip:=<your_robot_ip>
```
