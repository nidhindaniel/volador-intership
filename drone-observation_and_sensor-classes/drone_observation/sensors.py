
from numbers import Real

from .exceptions import InvalidSensorDataError

class SensorData:

    def __init__(self, sensor_name: str, value: float, unit: str):
        if not sensor_name.strip():
            raise InvalidSensorDataError("Sensor name cannot be empty.")
        if not isinstance(value, Real):
            raise InvalidSensorDataError("Sensor value must be a number.")
        if not unit.strip():
            raise InvalidSensorDataError("Sensor unit cannot be empty.")

        self.sensor_name = sensor_name
        self.value = value
        self.unit = unit

    def display(self) -> str:
        return f"{self.sensor_name}: {self.value} {self.unit}"


class TemperatureSensorData(SensorData):

    def __init__(self, value: float, unit: str = "°C"):
        super().__init__("Temperature", value, unit)


class HumiditySensorData(SensorData):

    def __init__(self, value: float):
        if not 0 <= value <= 100:
            raise InvalidSensorDataError("Humidity must be between 0 and 100 percent.")
        super().__init__("Humidity", value, "%")


class BatterySensorData(SensorData):

    def __init__(self, value: float):
        if value < 0:
            raise InvalidSensorDataError("Battery voltage cannot be negative.")
        super().__init__("Battery Voltage", value, "V")
