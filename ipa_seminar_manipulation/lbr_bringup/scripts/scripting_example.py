#!/usr/bin/env python
import roslib; roslib.load_manifest('lbr_bringup')
import rospy

from tf.transformations import *
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander, PlanningSceneInterface
 
### Helper function 
def gen_pose(frame_id="/base_link", pos=[0,0,0], euler=[0,0,0]):
	pose = PoseStamped()
	pose.header.frame_id = frame_id
	pose.header.stamp = rospy.Time.now()
	pose.pose.position.x, pose.pose.position.y, pose.pose.position.z = pos
	pose.pose.orientation.x, pose.pose.orientation.y, pose.pose.orientation.z, pose.pose.orientation.w = quaternion_from_euler(*euler)
	return pose

if __name__ == '__main__':
	rospy.init_node('scripting_example')
	while rospy.get_time() == 0.0: pass
	
	### Create a handle for the Planning Scene Interface
	psi = PlanningSceneInterface()
	rospy.sleep(1.0)
	
	### Create a handle for the Move Group Commander
	mgc = MoveGroupCommander("arm")
	rospy.sleep(1.0)
	
	
	### Add virtual obstacle
	pose = gen_pose(pos=[-0.2, -0.1, 1.2])
	psi.add_box("box", pose, size=(0.15, 0.15, 0.6))
	rospy.sleep(1.0)
	
	### Move to stored joint position
	mgc.set_named_target("left")
	mgc.go()
	
	### Move to Cartesian position
	goal_pose = gen_pose(pos=[0.123, -0.417, 1.361], euler=[3.1415, 0.0, 1.5707])
	mgc.go(goal_pose.pose)
	
	### Move Cartesian linear
	goal_pose.pose.position.z -= 0.1
	(traj,frac) = mgc.compute_cartesian_path([goal_pose.pose], 0.01, 4, True)
	mgc.execute(traj)
	
	print "Done"
