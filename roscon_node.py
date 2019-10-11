#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionGoal
from actionlib_msgs.msg import GoalID
from moveit_commander import RobotCommander, MoveGroupCommander
import termios
import threading
import sys
import moveit_commander
from visualization_msgs.msg import Marker
import select
import tty
import termios

class Pause():
	def __init__(self):
		self.goalid1 = GoalID()
		self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
		self.goal = MoveBaseGoal()
		self.id_goal = []
		self.Stop = True

		pass

	def state_start_up(self,):
		#do nothing
		a = 0
		print("Moving to state 1")

		return a


	def state_send_goals(self,flag1):
			# result = movebase_client(3.38,-0.17,0,0.999)

		if(flag1 == 0):
			flag1 = 1
			return -1.1,-0.02,0,0.017, flag1
		elif(flag1 == 1):
			flag1 = 2
			return 3.19,-0.19,0,0.999, flag1
		elif(flag1 == 2):
			flag1 = 0
			return -4.25,-2.93,0,0.99, flag1


	def state_movebase_client(self,x,y,z,w):
		self.client.wait_for_server()

		self.goal.target_pose.header.frame_id = "map"
		self.goal.target_pose.header.stamp = rospy.Time.now()
		self.goal.target_pose.pose.position.x = x
		self.goal.target_pose.pose.position.y = y
		self.goal.target_pose.pose.orientation.z = z
		self.goal.target_pose.pose.orientation.w = w
		self.visualization_markers(x,y,z,w)
		self.client.send_goal_and_wait(self.goal, rospy.Duration(30))


	def state_wait(self,flag3):
		now = 0
		now = rospy.Time.now().secs
	 	while(rospy.Time.now().secs < now+6):
	 		pass

		if(flag3 == 0):
			print("Moving to state 1")
			return True
		elif(flag3 == 1):
			print("Moving to state 2")
			return True
		elif(flag3 == 2):
			rospy.loginfo("Moving to state 3")
			return True

	def state_paused(self,):
		# cancel goal

		cancel_pub = rospy.Publisher('move_base/cancel', GoalID, queue_size=1)
		connections = cancel_pub.get_num_connections()
		try:
			goalId =self.id_goal[0]
			cancel_pub.publish(goalId)
		except IndexError:
			pass
		# client.wait_for_server()

	def goalid(self,msg):
		self.id_goal = []
		self.goalid1 = msg.goal_id
		if not self.goalid1.id :
			a =1
		else:
			self.id_goal.append(self.goalid1)

	def visualization_markers(self,x,y,z,w):
		mark = rospy.Publisher('Visualization_markers', Marker, queue_size=10)
		Markers = Marker()
		Markers.header.frame_id = "map"
		Markers.header.stamp = rospy.Time.now()
		Markers.ns = "goals"
		Markers.action = Markers.ADD
		Markers.type = Markers.ARROW
		Markers.id = 0
		Markers.scale.x = 0.5
		Markers.scale.y = 0.1
		Markers.scale.z = 0.1
		Markers.color.a = 1.0
		#markers.color.r = 1.0
		Markers.color.g = 0.5 
		Markers.color.b = 0.5
		Markers.pose.orientation.w =w
		Markers.pose.position.x = x
		Markers.pose.position.y = y 
		Markers.pose.position.z = 0.1
		Markers.id = 0
		mark.publish(Markers)





def main():
	global state
	global pause_active
	global flag1
	state = 0
	pause_active = False
	rospy.init_node('movebase_client_py')
	# robot = moveit_commander.RobotCommander()
	# scene = moveit_commander.PlanningSceneInterface()
	# group = moveit_commander.MoveGroupCommander("arm")
	# group.set_named_target("initial")
	# group.go()


	p = Pause()

	if(rospy.is_shutdown()):
		print("Came here")
		client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
		goal = MoveBaseGoal()
		client.cancel_goal()

	while not rospy.is_shutdown():
#state machine
		if state == 0:
			flag1 = p.state_start_up()
			state = 1
		elif state == 1:
			x,y,z,w,flag1 = p.state_send_goals(flag1)
			state = 2
		elif state == 2:
			tr = p.state_movebase_client(x,y,z,w)
			state = 3
		elif state == 3:
			sub = rospy.Subscriber('/move_base/goal',MoveBaseActionGoal, p.goalid)
			p.state_wait(flag1)
			state = 1


				

		#check if button p is pressed
		# if ...:
		# 	if not pause_active:
		# 		state = 4
		# 		pause_active = True
		# 	else:
		# 		state = 1
		# 		pause_active = False






if __name__ == '__main__':
	main()



	
