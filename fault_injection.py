def inject_fault(pressure, fault_type=None):

    if fault_type is None:
        return pressure

    if fault_type == "high":
        return 65.0

    elif fault_type == "low":
        return 35.0

    elif fault_type == "sensor_failure":
        return float("nan")

    else:
        raise ValueError("Unknown fault type")
