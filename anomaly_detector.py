def classify_pressure(pressure, lower_limit=45.0, upper_limit=55.0):
    if pressure < lower_limit or pressure > upper_limit:
        return "WARNING"

    return "NORMAL"
