import math
import pytest

from fault_injection import inject_fault

def test_normal_operation():
    result = inject_fault(50.0)
    assert result == 50.0


def test_high_pressure_fault():
    result = inject_fault(50.0, "high")
    assert result == 65.0


def test_low_pressure_fault():
    result = inject_fault(50.0, "low")
    assert result == 35.0


def test_sensor_failure():
    result = inject_fault(50.0, "sensor_failure")
    assert math.isnan(result)
