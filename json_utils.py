import json


def parse(text):
    """Parse a JSON string and return the Python object."""
    return json.loads(text)


def serialize(obj, indent=None):
    """Serialize a Python object to a JSON string."""
    return json.dumps(obj, indent=indent)


def validate(text):
    """Return True if *text* is valid JSON, False otherwise."""
    try:
        json.loads(text)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def merge(base, override):
    """Recursively merge *override* into *base* and return the result.

    Values in *override* take precedence.  Both arguments must be dicts.
    """
    if not isinstance(base, dict) or not isinstance(override, dict):
        raise TypeError("Both arguments must be dicts")
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge(result[key], value)
        else:
            result[key] = value
    return result
