class InvalidEndpointException(Exception):
    """Endpoint not known"""
    pass

class APIException(Exception):
    """Invalid status from API"""
    pass