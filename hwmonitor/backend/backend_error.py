class NoBackendFoundError(Exception):
    """This error should be raised if a module required an implemented vscreen, but None was found"""
