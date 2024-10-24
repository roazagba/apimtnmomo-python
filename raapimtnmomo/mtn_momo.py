from .config import MTNMoMoConfig
from .exceptions import *

class MTNMoMo:
    """
    MTNMoMo is a base class for handling common behaviors related to MTN MoMo API requests,
    such as exception handling based on API responses.
    """
    
    
    def __init__(self, config):
        """
        Initializes the MTNMoMo instance with the given configuration.
        
        :param config: An instance of MTNMoMoConfig containing API configuration details.
        """
        
        self.config = config

    def verif_exception(self, response):
        """
        Verifies the response status code and raises appropriate exceptions if errors are encountered.
        
        :param response: A tuple containing the status code and response data from an API request.
        :raises BadRequestException: If the status code is 400, indicating a bad request.
        :raises UnauthorizedException: If the status code is 401, indicating unauthorized access.
        :raises ConflictException: If the status code is 409, indicating a conflict, such as a duplicated reference ID.
        :raises InternalServerErrorException: If the status code is 500, indicating a server error.
        :raises MTNMoMoException: For other status codes, indicating an unspecified error.
        """
        
        status_code, data = response
        if status_code == 400:
            raise BadRequestException("Bad request, e.g. invalid data was sent in the request.")
        elif status_code == 401:
            raise UnauthorizedException("Unauthorized")
        elif status_code == 409:
            raise ConflictException(f"Conflict, duplicated reference id: {data}")
        elif status_code == 500:
            raise InternalServerErrorException(f"Internal Server Error: {data}")
        else:
            raise MTNMoMoException("Another error")
