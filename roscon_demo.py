import roslaunch
import select
import tty
import termios
import sys
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionGoal
from actionlib_msgs.msg import GoalID




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

if __name__ == '__main__':
	pause = True
	rospy.init_node('Pausing node', anonymous=True)
	uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
	roslaunch.configure_logging(uuid)

	while True:
		with NonBlockingConsole() as nbc:
			if nbc.get_data() == 'p' and pause == True:
				launch = roslaunch.parent.ROSLaunchParent(uuid, ["//home/pradheep/neobotix_workspace/src/neo_simulation/launch/mmo_700/roscon_demo.launch"])
				launch.start()
				pause = False

			elif nbc.get_data() == 'p' and pause == False:
				rospy.loginfo("Manual control will be given to you in 5seconds")
				cancel_pub = rospy.Publisher('move_base/cancel', GoalID, queue_size=1)
				goalId = GoalID()
				cancel_pub.publish(goalId)
				launch.shutdown()
				pause = True

