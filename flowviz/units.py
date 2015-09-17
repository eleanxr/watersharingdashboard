
rate_volume_abbr = {
    "cfs": "ft^3",
    "afd": "af",
}

def get_volume_unit(rate_unit):
    """Get the volume unit for a given rate unit."""
    return rate_volume_abbr.get(rate_unit.lower(), None)
