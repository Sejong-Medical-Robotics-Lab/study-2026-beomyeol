import rclpy
from rclpy.node import Node
from std_msgs.mssg import String
class Replier(Node):
    def __init__(self):
        super().__inint__("replier")
        self.sub = self.create_subscription(
            String, "greeting", self.on_msg, 10)
        
    def on_msg(self, msg):
        self.get_logger().info(f"받았습니다: {msg.data}")

def main():
    rclpy.init()
    rclpy.spin(Replier())
if __name__ == "__main__":
    main()