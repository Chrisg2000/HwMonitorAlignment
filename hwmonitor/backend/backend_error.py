class NoBackendFoundError(Exception):
    """This error should be raised if a module required an implemented monitor_model_adapter, but None was found"""
