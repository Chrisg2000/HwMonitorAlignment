class ApplyChangesFailedError(OSError):
    """This error should be raised if the changes on the local application model
    cannot be applied to the os display device item
    """
    pass


class SyncMonitorError(OSError):
    """This error should be raised if the process of requesting updated information  failed
    """
    pass
