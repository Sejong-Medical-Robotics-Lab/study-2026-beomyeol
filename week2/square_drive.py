#!/usr/bin/env python3

import math
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class SquareDriveNode(Node):
    """Publish cmd_vel commands to drive a 1 m square."""

    def __init__(self) -> None:
        super().__init__("square_drive_node")

        # 실제 시뮬레이터 토픽이 다르면 이 값을 수정한다.
        self.publisher = self.create_publisher(Twist, "/cmd_vel", 10)

        # 사각형 설정값
        self.side_length = 1.0       # 한 변 길이 [m]
        self.linear_speed = 0.3      # 전진 속도 [m/s]
        self.angular_speed = 0.5     # 회전 각속도 [rad/s]
        self.publish_rate = 20.0     # 명령 재전송 주기 [Hz]

        # 이론적인 이동 시간
        self.forward_time = self.side_length / self.linear_speed
        self.turn_time = (math.pi / 2.0) / self.angular_speed

        self.get_logger().info(
            f"전진 시간: {self.forward_time:.2f}초, "
            f"90도 회전 시간: {self.turn_time:.2f}초"
        )

    def publish_velocity(
        self,
        linear_x: float,
        angular_z: float,
        duration: float,
    ) -> None:
        """Publish the same velocity repeatedly for the requested duration."""

        command = Twist()
        command.linear.x = linear_x
        command.angular.z = angular_z

        start_time = time.monotonic()
        period = 1.0 / self.publish_rate

        while rclpy.ok() and time.monotonic() - start_time < duration:
            self.publisher.publish(command)
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(period)

    def stop(self, duration: float = 0.5) -> None:
        """Repeatedly publish zero velocity to ensure the robot stops."""

        self.get_logger().info("정지")

        stop_command = Twist()
        period = 1.0 / self.publish_rate
        end_time = time.monotonic() + duration

        while rclpy.ok() and time.monotonic() < end_time:
            self.publisher.publish(stop_command)
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(period)

    def run_square(self) -> None:
        """Drive four sides and make four 90-degree left turns."""

        self.get_logger().info("3초 후 사각형 주행을 시작합니다.")
        time.sleep(3.0)

        for side in range(1, 5):
            self.get_logger().info(
                f"{side}번째 변: {self.side_length:.1f} m 전진"
            )

            self.publish_velocity(
                linear_x=self.linear_speed,
                angular_z=0.0,
                duration=self.forward_time,
            )
            self.stop()

            self.get_logger().info(
                f"{side}번째 회전: 왼쪽으로 약 90도 회전"
            )

            self.publish_velocity(
                linear_x=0.0,
                angular_z=self.angular_speed,
                duration=self.turn_time,
            )
            self.stop()

        self.get_logger().info("사각형 주행 완료")


def main(args=None) -> None:
    rclpy.init(args=args)
    node = SquareDriveNode()

    try:
        node.run_square()
    except KeyboardInterrupt:
        node.get_logger().warning("사용자가 실행을 중단했습니다.")
    finally:
        # 중간에 Ctrl+C를 눌러도 마지막 정지 명령을 보낸다.
        if rclpy.ok():
            node.stop(duration=1.0)

        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()