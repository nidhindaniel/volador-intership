"""Custom exceptions for the drone observation package."""


class DroneObservationError(Exception):
    """Base exception for errors raised by this package."""


class InvalidSensorDataError(DroneObservationError):
    """Raised when a sensor reading is not valid."""


class InvalidObservationError(DroneObservationError):
    """Raised when drone observation details are not valid."""
