#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import time
import pdb
import numpy

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg


# Initialize app
try:
    app = qi.Application(url='tcp://192.168.1.2:9559')
except RuntimeError:
    print ("Can't connect to Pepper")
    sys.exit(1)
ls = []
app.start()
session = app.session

def start(service, session = session):
	ls.append(service) if service not in ls else ls
	return session.service(service)

faceCharacteristic = start('ALFaceCharacteristics')
notification = start('ALNotificationManager')
autonomousLife = start('ALAutonomousLife')
callback = start('ALExpressionWatcher')
speech = start('ALSpeechRecognition')
tactile = start('ALTactileGesture')
navigation = start('ALNavigation')
posture = start('ALRobotPosture')
recharge = start('ALRecharge')
tts = start('ALTextToSpeech')
battery = start('ALBattery')
memory = start('ALMemory')
motion = start('ALMotion')
mood = start('ALMood')

def battery(tts = tts, battery = battery):
    tts.setParameter("pitchShift", 1)
    tts.setParameter('volume',20)
    tts.say('I have' + str(battery.getBatteryCharge()) + 'per cent remaining')


# Functions to make things easier

# Breakpoint





class pepper(object):
  def __init__(self):
    super(pepper, self).__init__()
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    group_name = "left_arm"
    move_group = moveit_commander.MoveGroupCommander(group_name)
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                   moveit_msgs.msg.DisplayTrajectory,
                                                   queue_size=20)

    planning_frame = move_group.get_planning_frame()
    print "============ Planning frame: %s" % planning_frame
    eef_link = move_group.get_end_effector_link()
    print "============ End effector link: %s" % eef_link
    group_names = robot.get_group_names()
    print "============ Available Planning Groups:", robot.get_group_names()
    print "============ Printing robot state"
    print robot.get_current_state()
    print ""
    move_group.set_planning_time(3)

    self.box_name = ''
    self.robot = robot
    self.scene = scene
    self.move_group = move_group
    self.display_trajectory_publisher = display_trajectory_publisher
    self.planning_frame = planning_frame
    self.eef_link = eef_link
    self.group_names = group_names


  def move(self, j0, j1, j2 ,j3 ,j4):
    joint_goal = self.move_group.get_current_joint_values()
    joint_goal[0] = j0
    joint_goal[1] = j1
    joint_goal[2] = j2
    joint_goal[3] = j3
    joint_goal[4] = j4
    start_time = time.time()
    plan = self.move_group.plan(joint_goal)
    end_time = time.time()
    plan_time = end_time - start_time
    self.move_group.execute(plan, wait=True)
    end_time2 = time.time()
    execute_time = end_time2 - end_time

    print("Planning time: " + str(plan_time))
    print("Execution time: " + str(execute_time))




  def go_to_pose_goal(self, x, y, z, qw, qx, qy, qz):
    move_group = self.move_group

    pose_goal = geometry_msgs.msg.Pose()
    pose_goal.orientation.w = qw
    pose_goal.orientation.x = qx
    pose_goal.orientation.y = qy
    pose_goal.orientation.z = qz
    pose_goal.position.x = x
    pose_goal.position.y = y
    pose_goal.position.z = z

    move_group.set_pose_target(pose_goal)
    plan = move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

    current_pose = self.move_group.get_current_pose().pose
    return 1


  def plan_cartesian_path(self, scale=1):
    move_group = self.move_group
    waypoints = []
    wpose = move_group.get_current_pose().pose
    wpose.position.z -= scale * 0.1  
    wpose.position.y += scale * 0.2  
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.x += scale * 0.1  
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.y -= scale * 0.1  
    waypoints.append(copy.deepcopy(wpose))

    (plan, fraction) = move_group.compute_cartesian_path(
                                       waypoints,   
                                       0.01,        
                                       0.0)         
    return plan, fraction



  def display_trajectory(self, plan):
    robot = self.robot
    display_trajectory_publisher = self.display_trajectory_publisher
    display_trajectory = moveit_msgs.msg.DisplayTrajectory()
    display_trajectory.trajectory_start = robot.get_current_state()
    display_trajectory.trajectory.append(plan)
    display_trajectory_publisher.publish(display_trajectory);


  def execute_plan(self, plan):
    move_group = self.move_group
    move_group.execute(plan, wait=False)



def main():
	time.sleep(2)
	peppers = pepper()
	# peppers.move(0,1.2,-1.55,-1.5,0)
	x = -1
	y = -1
	z = -1
	while 1:
		z += 0.1
		x += 0.1
		y += 0.1
		# print "Current pose: ",peppers.move_group.get_current_pose()
		peppers.go_to_pose_goal(-0.1,0.3,0.6,0.74,-0.485,0.41,0.21)
		time.sleep(0.5)
	# tts.say("Hey there")
	# peppers.move(1.33456337452, 0.0337476730347, -1.5508544445, -0.0276699256897, 0.214718103409)


if __name__=='__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass

