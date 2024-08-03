
class ResponseDTO:
    def __init__(self, status, message = None, data = None, **kwargs):
        self.data = data
        self.status = status
        self.message = message
        self.error_code = kwargs.get("error_code")