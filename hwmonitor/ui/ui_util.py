def index_from_device_name(device_name: str) -> str:
    """Convert MS Windows device_name to an index.

    If device_name does not fit the pattern an empty string is returned
    """
    device_name_pattern = r"\\.\DISPLAY"
    if device_name.startswith(device_name_pattern):
        return device_name[len(device_name_pattern):]
    return ''
