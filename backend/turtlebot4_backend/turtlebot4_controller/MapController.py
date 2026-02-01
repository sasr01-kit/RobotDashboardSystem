import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
import numpy as np
import json
import matplotlib.pyplot as plt
import os


class MapSubscriber(Node):
    def __init__(self):
        super().__init__('map_subscriber')

        # QoS for latched /map topic
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
            durability=rclpy.qos.QoSDurabilityPolicy.TRANSIENT_LOCAL
        )

        self.subscription = self.create_subscription(
            OccupancyGrid,
            '/map',
            self.callback,
            qos_profile
        )

        # Directory to save files
        self.save_dir = '/home/saadhvi/ros2_ws/src/map_only_launch'
        os.makedirs(self.save_dir, exist_ok=True)

    def callback(self, msg: OccupancyGrid):
        # Log that the map was received
        self.get_logger().info('Map received!')

        # Convert flat OccupancyGrid to 2D NumPy array
        width = msg.info.width
        height = msg.info.height
        grid = np.array(msg.data, dtype=int).reshape((height, width))

        # ----- Save as JSON -----
        json_path = os.path.join(self.save_dir, 'warehouse_map.json')
        map_json = {
            "width": width,
            "height": height,
            "resolution": msg.info.resolution,
            "origin": {
                "x": msg.info.origin.position.x,
                "y": msg.info.origin.position.y,
                "z": msg.info.origin.position.z
            },
            "data": grid.tolist()
        }

        with open(json_path, 'w') as f:
            json.dump(map_json, f, indent=2)
        self.get_logger().info(f'Occupancy grid saved as {json_path}')

        # ----- Save as heatmap PNG -----
        visual_grid = grid.copy()
        visual_grid[visual_grid == -1] = 50  # unknowns -> middle gray

        png_path = os.path.join(self.save_dir, 'warehouse_map.png')
        plt.figure(figsize=(8, 8))
        plt.imshow(visual_grid, cmap='gray_r', origin='lower')
        plt.colorbar(label='Occupancy Value')
        plt.title('Warehouse Occupancy Grid Heatmap')
        plt.savefig(png_path)
        plt.close()
        self.get_logger().info(f'Occupancy grid heatmap saved as {png_path}')


def main(args=None):
    rclpy.init(args=args)
    node = MapSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
