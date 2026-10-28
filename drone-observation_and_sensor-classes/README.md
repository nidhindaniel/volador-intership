# Drone Observation and Sensor Classes

This Python program models a drone observation and its sensor readings as a reusable Python package.

## Package layout

```text
drone_observation/
├── __init__.py       # Exports public classes
├── exceptions.py     # Custom exceptions
├── observation.py    # DroneObservation class
└── sensors.py        # Base and specialised sensor classes
```

## Classes

### `SensorData`

Represents one measurement collected by a sensor.

| Attribute | Description |
| --- | --- |
| `sensor_name` | Name of the sensor or measurement |
| `value` | Recorded measurement value |
| `unit` | Unit used for the value |

Method: `display()` returns the sensor name, value, and unit as text.

`TemperatureSensorData`, `HumiditySensorData`, and `BatterySensorData` inherit from `SensorData`. This demonstrates inheritance while giving each sensor type its own default name, unit, and validation rules.

### `DroneObservation`

Represents a drone and the details of one observation.

| Attribute | Description |
| --- | --- |
| `drone_id` | Unique drone identifier |
| `latitude` | Drone latitude |
| `longitude` | Drone longitude |
| `altitude` | Drone altitude in metres |
| `sensor_data` | List of attached `SensorData` objects |

Methods:

- `add_sensor_data(sensor)`: adds a sensor-reading object to the observation.
- `display_observation()`: prints the drone details and every attached sensor reading.

## Objects created

The program creates these `SensorData` objects:

- `temperature_sensor`: Temperature, `32.5 °C`
- `humidity_sensor`: Humidity, `68 %`
- `battery_sensor`: Battery Voltage, `11.7 V`

It also creates one `DroneObservation` object named `drone` with ID `DRONE-001`, location `9.4981, 76.3388`, and altitude `120.5 m`.

Each sensor object is added to `drone`. Finally, `drone.display_observation()` displays the complete observation.

## concepts used

- **Classes:** `SensorData`, its sensor subclasses, and `DroneObservation` model the domain.
- **Inheritance:** the three specialised sensor classes extend `SensorData`.
- **Composition:** a `DroneObservation` owns a list of `SensorData` objects.
- **Exceptions:** invalid data raises `InvalidSensorDataError` or `InvalidObservationError`.
- **Modular packages:** the related code is organised under the `drone_observation` package and imported by `code.py`.

## Run

From this folder, run:

```bash
python code.py
```
