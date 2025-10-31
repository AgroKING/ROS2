import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class HeadlessTurtleSim(Node):
    def __init__(self):
        super().__init__('headless_turtle_sim')

        # Start the turtle in the "center"
        self.pose_ = Pose()
        self.pose_.x = 5.54
        self.pose_.y = 5.54
        self.pose_.theta = 0.0

        # Store the last received command
        self.last_cmd_vel_ = Twist()

        # Create publisher for the pose
        self.pose_publisher_ = self.create_publisher(Pose, '/turtle1/pose', 10)

        # Create subscriber for velocity commands
        self.cmd_vel_subscriber_ = self.create_subscription(
            Twist,
            '/turtle1/cmd_vel',
            self.cmd_vel_callback,
            10)

        # Create a timer to run the simulation update loop
        self.update_timer_ = self.create_timer(0.01, self.update_pose) # Run at 100Hz
        self.last_update_time_ = self.get_clock().now()

        self.get_logger().info(' Turtle Sim has started.')

    def cmd_vel_callback(self, msg):
        # Store the latest velocity command
        self.last_cmd_vel_ = msg

    def update_pose(self):
        now = self.get_clock().now()
        dt = (now - self.last_update_time_).nanoseconds / 1e9 # Delta time in seconds

        # Apply physics
        new_theta = self.pose_.theta + self.last_cmd_vel_.angular.z * dt
        new_x = self.pose_.x + self.last_cmd_vel_.linear.x * math.cos(new_theta) * dt
        new_y = self.pose_.y + self.last_cmd_vel_.linear.x * math.sin(new_theta) * dt

        # Update the pose
        self.pose_.x = new_x
        self.pose_.y = new_y
        self.pose_.theta = new_theta
        self.pose_.linear_velocity = self.last_cmd_vel_.linear.x
        self.pose_.angular_velocity = self.last_cmd_vel_.angular.z

        # Publish the new pose
        self.pose_publisher_.publish(self.pose_)

        # Update the last update time
        self.last_update_time_ = now

def main(args=None):
    rclpy.init(args=args)
    node = HeadlessTurtleSim()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
