
from numbers import Real

from .exceptions import InvalidObservationError, InvalidSensorDataError
from .sensors import SensorData


class DroneObservation:
    """A drone's location and its composed collection of sensor data."""

    def __init__(
        self,
        drone_id: str,
        latitude: float,
        longitude: float,
        altitude: float,
    ):
        if not drone_id.strip():
            raise InvalidObservationError("Drone ID cannot be empty.")
        if not isinstance(latitude, Real) or not -90 <= latitude <= 90:
            raise InvalidObservationError("Latitude must be between -90 and 90.")
        if not isinstance(longitude, Real) or not -180 <= longitude <= 180:
            raise InvalidObservationError("Longitude must be between -180 and 180.")
        if not isinstance(altitude, Real):
            raise InvalidObservationError("Altitude must be a number.")

        self.drone_id = drone_id
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.sensor_data: list[SensorData] = []

    def add_sensor_data(self, sensor: SensorData) -> None:
        """Add a SensorData object to this observation."""
        if not isinstance(sensor, SensorData):
            raise InvalidSensorDataError("Only SensorData objects can be added.")
        self.sensor_data.append(sensor)

    def display_observation(self) -> None:
        """Print the drone details and all composed sensor readings."""
        print("\nDrone Observation")
        print("-----------------")
        print(f"Drone ID: {self.drone_id}")
        print(f"Latitude: {self.latitude}")
        print(f"Longitude: {self.longitude}")
        print(f"Altitude: {self.altitude} m")
        print("\nSensor Readings:")

        for sensor in self.sensor_data:
            print(sensor.display())
