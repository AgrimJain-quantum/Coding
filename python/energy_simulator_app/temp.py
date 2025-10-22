# task1c.py
# This script controls a UR5 robotic arm to move through three predefined waypoints
# using the moveit_servo package in ROS 2.

import rclpy
from rclpy.node import Node
from rclpy.logging import get_logger

from geometry_msgs.msg import PoseStamped
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from math import sqrt, acos, fabs
import time

class ArmController(Node):
    """
    A ROS 2 Node to control the UR5 arm using moveit_servo.
    It moves the arm through a series of predefined waypoints, pausing at each one.
    """
    def __init__(self):
        super().__init__('task1c_arm_controller')

        # Publisher to send target poses to the servoing node
        self.pose_publisher = self.create_publisher(PoseStamped, '/servo_node/pose_target_cmds', 10)

        # TF2 listener to get the current pose of the end-effector
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Tolerances for considering a waypoint reached
        self.pos_tolerance = 0.15  # meters
        self.ori_tolerance = 0.15  # radians

        self.get_logger().info('Arm Controller Node has been started.')

    def calculate_pose_error(self, current_transform, target_pose):
        """
        Calculates the Euclidean distance for position and the angular distance
        for orientation between the current and target poses.
        """
        # Position error (Euclidean distance)
        pos_current = current_transform.translation
        pos_target = target_pose.position
        
        position_error = sqrt(
            (pos_target.x - pos_current.x)**2 +
            (pos_target.y - pos_current.y)**2 +
            (pos_target.z - pos_current.z)**2
        )

        # Orientation error (angular distance between quaternions)
        q_current = current_transform.rotation
        q_target = target_pose.orientation
        
        dot_product = q_current.x * q_target.x + \
                      q_current.y * q_target.y + \
                      q_current.z * q_target.z + \
                      q_current.w * q_target.w
        
        # Use fabs() to handle potential floating point inaccuracies near 1
        orientation_error = 2 * acos(fabs(dot_product))

        return position_error, orientation_error

    def move_to_pose(self, target_pose_stamped):
        """
        Continuously publishes the target pose and waits until the arm's end-effector
        reaches the destination within the specified tolerance.
        """
        waypoint_info = (f"x={target_pose_stamped.pose.position.x:.3f}, "
                         f"y={target_pose_stamped.pose.position.y:.3f}, "
                         f"z={target_pose_stamped.pose.position.z:.3f}")
        self.get_logger().info(f"Moving to waypoint: [{waypoint_info}]")

        # Loop until the target is reached
        while rclpy.ok():
            # The servo node requires a continuous stream of commands to generate smooth motion
            self.pose_publisher.publish(target_pose_stamped)

            try:
                # Get the current transform from the robot's base to its end-effector (tool0)
                now = rclpy.time.Time()
                transform_stamped = self.tf_buffer.lookup_transform(
                    'base',       # Target frame (Corrected from 'base_link')
                    'tool0',      # Source frame (End-effector)
                    now,
                    timeout=rclpy.duration.Duration(seconds=0.5)
                )
                current_transform = transform_stamped.transform

            except Exception as e:
                self.get_logger().warn(f"Could not get transform: {e}, retrying...")
                time.sleep(0.1)
                continue

            # Check if the arm is within the tolerance for both position and orientation
            pos_err, ori_err = self.calculate_pose_error(current_transform, target_pose_stamped.pose)

            if pos_err < self.pos_tolerance and ori_err < self.ori_tolerance:
                self.get_logger().info("Waypoint reached successfully!")
                break

            time.sleep(0.1) # Control the loop rate to avoid spamming

def main(args=None):
    rclpy.init(args=args)
    arm_controller = ArmController()

    # Allow some time for nodes to initialize and the TF buffer to populate
    time.sleep(4.0)
    
    # --- Define the 3 Waypoints ---

    # P1: [-0.214, -0.532, 0.557] | Orientation: [0.707, 0.028, 0.034, 0.707]
    p1 = PoseStamped()
    p1.header.frame_id = "base_Link" # The reference frame for the pose
    p1.header.stamp = arm_controller.get_clock().now().to_msg()
    p1.pose.position.x = -0.214
    p1.pose.position.y = -0.532
    p1.pose.position.z = 0.557
    p1.pose.orientation.x = 0.707
    p1.pose.orientation.y = 0.028
    p1.pose.orientation.z = 0.034
    p1.pose.orientation.w = 0.707

    # P2: [-0.159, 0.501, 0.415] | Orientation: [0.029, 0.997, 0.045, 0.033]
    p2 = PoseStamped()
    p2.header.frame_id = "base"
    p2.header.stamp = arm_controller.get_clock().now().to_msg()
    p2.pose.position.x = -0.159
    p2.pose.position.y = 0.501
    p2.pose.position.z = 0.415
    p2.pose.orientation.x = 0.029
    p2.pose.orientation.y = 0.997
    p2.pose.orientation.z = 0.045
    p2.pose.orientation.w = 0.033

    # P3: [-0.806, 0.010, 0.182] | Orientation: [-0.684, 0.726, 0.05, 0.008]
    p3 = PoseStamped()
    p3.header.frame_id = "base"
    p3.header.stamp = arm_controller.get_clock().now().to_msg()
    p3.pose.position.x = -0.806
    p3.pose.position.y = 0.010
    p3.pose.position.z = 0.182
    p3.pose.orientation.x = -0.684
    p3.pose.orientation.y = 0.726
    p3.pose.orientation.z = 0.050
    p3.pose.orientation.w = 0.008
    
    waypoints = [p1, p2, p3]

    # --- Execute the Waypoint Sequence ---
    for i, waypoint in enumerate(waypoints):
        arm_controller.get_logger().info(f"--- Processing Waypoint {i+1} ---")
        waypoint.header.stamp = arm_controller.get_clock().now().to_msg()
        arm_controller.move_to_pose(waypoint)
        
        # Pause at the waypoint as required by the task
        arm_controller.get_logger().info("Pausing for 1 second at waypoint.")
        time.sleep(1.0)

    arm_controller.get_logger().info("All waypoints visited. Task complete.")
    arm_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
