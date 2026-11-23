import pytest
from anomaly_detector import classify_pressure


def test_normal_pressure():
    assert classify_pressure(50.0) == "NORMAL"


def test_high_pressure():
    assert classify_pressure(65.0) == "WARNING"


def test_low_pressure():
    assert classify_pressure(40.0) == "WARNING"


def test_boundary_values():
    assert classify_pressure(45.0) == "NORMAL"
    assert classify_pressure(55.0) == "NORMAL"

def test_invalid_sensor_reading():
    with pytest.raises(ValueError):
        classify_pressure(float("nan"))
