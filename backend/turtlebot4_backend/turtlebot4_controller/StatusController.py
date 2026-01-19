import rclpy
from rclpy.node import Node

from sensor_msgs.msg import BatteryState
from turtlebot4_msgs.msg import DockStatus


class StatusController(Node):
    def __init__(self):
        super().__init__('status_controller')

        # Battery subscription
        self.battery_sub = self.create_subscription(
            BatteryState,
            '/battery_state',
            self.battery_callback,
            10
        )

        # Dock status subscription
        self.dock_sub = self.create_subscription(
            DockStatus,
            '/dock_status',
            self.dock_callback,
            10
        )

        # Stored state
        self.battery_percentage = None
        self.is_docked = None

        self.get_logger().info(
            'StatusController started, listening to /battery_state and /dock_status'
        )

    def battery_callback(self, msg: BatteryState):
        self.battery_percentage = msg.percentage
        self.display_status()

    def dock_callback(self, msg: DockStatus):
        # 0 = UNKNOWN, 1 = UNDOCKED, 2 = DOCKED, 3 = DOCKING, 4 = UNDOCKING
        self.is_docked = msg.dock_state
        self.display_status()

    def display_status(self):
        if self.battery_percentage is None or self.is_docked is None:
            return

        dock_state_str = {
            0: "UNKNOWN",
            1: "UNDOCKED",
            2: "DOCKED",
            3: "DOCKING",
            4: "UNDOCKING"
        }.get(self.is_docked, "INVALID")

        self.get_logger().info(
            f"Battery: {self.battery_percentage * 100:.1f}%, "
            f"Dock: {dock_state_str}"
        )


def main(args=None):
    rclpy.init(args=args)

    node = StatusController()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()
