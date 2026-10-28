from drone_observation import BatterySensorData
from drone_observation import DroneObservation
from drone_observation import HumiditySensorData
from drone_observation import TemperatureSensorData

def main():
    """Create a drone observation and attach its sensor readings."""
    temperature_sensor = TemperatureSensorData(32.5)
    humidity_sensor = HumiditySensorData(68)
    battery_sensor = BatterySensorData(11.7)

    # Composition: a DroneObservation contains SensorData objects.
    drone = DroneObservation(
        drone_id="DRONE-001",
        latitude=9.4981,
        longitude=76.3388,
        altitude=120.5,
    )

    drone.add_sensor_data(temperature_sensor)
    drone.add_sensor_data(humidity_sensor)
    drone.add_sensor_data(battery_sensor)
    drone.display_observation()


if __name__ == "__main__":
    main()
