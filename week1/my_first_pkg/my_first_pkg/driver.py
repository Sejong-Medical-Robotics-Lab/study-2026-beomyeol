import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TurtleDriver(Node):

    def __init__(self):
        super().__init__('turtle_driver')

        self.publisher_ = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.timer = self.create_timer(0.1, self.publish_velocity)

    def publish_velocity(self):
        msg = Twist()

        # 앞으로 이동하는 속도
        msg.linear.x = 2.0

        # 회전하는 속도
        msg.angular.z = 1.8

        self.publisher_.publish(msg)

        self.get_logger().info(
            f'linear.x={msg.linear.x}, angular.z={msg.angular.z}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = TurtleDriver()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()