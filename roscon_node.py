#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionGoal
from actionlib_msgs.msg import GoalID
import termios
import threading
import sys
import select
import tty
import termios



class NonBlockingConsole(object):

	def __enter__(self):
		self.old_settings = termios.tcgetattr(sys.stdin)
		tty.setcbreak(sys.stdin.fileno())
		return self

	def __exit__(self, type, value, traceback):
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)


	def get_data(self):
		if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
			return sys.stdin.read(1)
		return False


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
			return -5,0,0,0.1, flag1
		elif(flag1 == 1):
			flag1 = 2
			return 5,0,0,0.1, flag1
		elif(flag1 == 2):
			flag1 = 0
			return -3,0,0,0.1, flag1


	def state_movebase_client(self,x,y,z,w):
		self.client.wait_for_server()

		self.goal.target_pose.header.frame_id = "map"
		self.goal.target_pose.header.stamp = rospy.Time.now()
		self.goal.target_pose.pose.position.x = x
		self.goal.target_pose.pose.position.y = y
		self.goal.target_pose.pose.orientation.z = z
		self.goal.target_pose.pose.orientation.w = w
		self.client.send_goal(self.goal)
		while self.client.get_state()!=actionlib.GoalStatus.SUCCEEDED:
			pass

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
			print("Moving to state 3")
			return True

	def state_paused(self,):
		# cancel goal
		# client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
		# goal = MoveBaseGoal()
		# client.cancel_goal()
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

def main():
	global state
	global pause_active
	global flag1
	state = 0
	pause_active = False
	rospy.init_node('movebase_client_py')
	p = Pause()

	with NonBlockingConsole() as nbc:
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
			elif state == 4:
				p.state_paused()
				if nbc.get_data() == '\x1b' and pause_active == True: 
					state = 1
					flag1 = 0
					pause_active = False
					print("Unpausing the system")
			else:
				print "ERROR"
				
			if nbc.get_data() == '\x1b' and pause_active == False: 
				print("pausing the system")
				state = 4
				pause_active = True
				pressed = True	



				

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

	
