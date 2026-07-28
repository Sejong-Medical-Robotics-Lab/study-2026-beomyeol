import rclpy
from rclpy.node import Node
from std_msgs.msg import String
class Greeter(Node):
    def __init__(self):

        super().__init__("greeter")
        self.pub = self.create_publisher(String, "greeting", 10)
        self.timer = self.create_timer(1.0, self.tick)
        self.count = 0

    def tick(self):
        msg = String()
        msg.data = f"Hello ROS2! ({self.count})"
        self.pub.publish(msg)

        self.count += 1
        
def main():
    rclpy.init()
    rclpy.spin(Greeter())

if __name__ == "_main_":
    main()
