import numpy as np
from typing import Optional
import threading
from turtlebot4_backend.turtlebot4_model.Map import Map
from turtlebot4_backend.turtlebot4_model.MapData import MapData
from turtlebot4_backend.turtlebot4_controller.RosbridgeConnection import RosbridgeConnection

class MapController:
    """
    Receives the static OccupancyGrid map via ROSBridge,
    converts it into a MapData object, and injects it into the Map model.
    """

    def __init__(
        self,
        map_model: Map,
        rosbridge_host: str = 'localhost',
        rosbridge_port: int = 9090
    ) -> None:
        self._map_model = map_model
        self._map_received = False

        # ROSBridge connection
        self._ros = RosbridgeConnection(host=rosbridge_host, port=rosbridge_port)

    # loadMap(source: String) : void 
    # is now a manual action as we discovered that you have to run the map server (ros2 run ...) in terminal
    # for the intended functionality.
    # 
    # updateHumanPositions(msg: Dictionary) : void
    # computeProxemicDistance(humanId: String) : void 
    # are both depending on the human model from the fuzzy_social_controller package, which was not communicated.
    # Thus, the implementation of these will be the client's responsibility. 
    #
    # These changes are documented in our implementation document.

    def subscribeToMap(self) -> None:
        """Connect to rosbridge and subscribe to the /map topic."""
        def _connect_and_subscribe():
            try:
                self._ros.connect()
            except Exception as e:
                print(f"Failed to connect to rosbridge: {e}")
                return

            print("MapController connected to rosbridge.")

            try:
                self._ros.subscribe('/map', 'nav_msgs/OccupancyGrid', self._map_callback)
                print("Subscribed to /map topic.")
            except Exception as e:
                print(f"Failed to subscribe to /map topic: {e}")

        threading.Thread(target=_connect_and_subscribe, daemon=True).start()

    def _map_callback(self, message: dict) -> None:
        """
        Handles the OccupancyGrid message received from rosbridge.
        This should only run once for the static map.
        """
        if self._map_received:
            return  # Ignore further updates

        print("Static map received from ROSBridge")

        info = message['info']

        resolution = info['resolution']
        width_cells = info['width']
        height_cells = info['height']

        # Convert to meters (consistent with your Map logic)
        width_m = width_cells * resolution
        height_m = height_cells * resolution

        occupancy_grid = list(message['data'])  # flat list[int]

        # Create MapData instance
        map_data = MapData(
            resolution=resolution,
            width=width_m,
            height=height_m,
            occupancyGrid=occupancy_grid
        )

        # Inject into Map model (this triggers PNG + base64 conversion)
        self._map_model.set_mapData(map_data)

        self._map_received = True

        print("MapData injected into Map model")

        # Optional: unsubscribe since map is static
        self._ros.unsubscribe('/map')

    def shutdown(self) -> None:
        """
        Clean shutdown of rosbridge connection.
        """
        try:
            self._ros.terminate()
        except Exception as e:
            print(f"Error during shutdown: {e}")
        print("MapController shutdown complete")
