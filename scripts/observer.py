#!/usr/bin/python
import rospy
import actionlib
import numpy
from sensor_msgs.msg import JointState
from sensor_msgs.msg import CameraInfo
from ensenso_camera_msgs.msg import RequestDataAction, RequestDataActionGoal, RequestDataActionResult

class observer(object):
    def __init__(self):

        self.trigger_goal  = False
        self.trigger_result = False
        self.compare = False
        self.count = 0
        self.init_state = []
        self.vel = []
        self.goal_sub = rospy.Subscriber("request_data/goal", RequestDataActionGoal, self.goal_cb)
        self.result_sub = rospy.Subscriber("request_data/result", RequestDataActionResult, self.result_cb)
        self.joint_state_sub = None

    def goal_cb(self,msg):
        # callback to subscribe for the action goal
        self.trigger_goal = True

    def result_cb(self,msg):
        # callback to subscribe for the action result
        self.trigger_result = True

    def joint_state_cb(self,msg):
        # callback to subscribe for the joint state position
        # print("\n")
        # print(msg.position)
        self.vel.append(msg.velocity)


    def cycle(self):
        # Black box
        if self.trigger_goal == True:
            print("\nCamera started capturing")
            print("I am monitoring the joints")
            self.js_sub = rospy.Subscriber("/prbt/joint_states",JointState, self.joint_state_cb)
            self.trigger_goal  = False

        if self.trigger_result == True:
            self.js_sub.unregister()
            # count number of captures
            self.count = self.count+1
            # check for the vibration
            self.compare = all(x == self.vel[0] for x in self.vel)
            self.init_state.append(self.compare)
            print("Not moving = %r"%self.compare)
            self.compare = False
            print("camera stopped capturing\n")
            self.trigger_result = False
            self.vel = []

        if self.count == 4:
            print(self.init_state)
            self.count = 0
            self.init_state = []

    def create_problem(self):
        pass

def main():

    rospy.init_node('observer_node')
    obs = observer()

    while not rospy.is_shutdown():
        obs.cycle()
        # rospy.sleep(0.01)
        rate = rospy.Rate(10)
        rate.sleep()




if __name__ == "__main__":
    main()
