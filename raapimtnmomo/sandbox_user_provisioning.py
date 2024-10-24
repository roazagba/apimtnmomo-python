from .requestss import Request
from .exceptions import *
import json

class SandboxUserProvisioning:
    """
    A class that handles provisioning sandbox users for the MTN MoMo API.
    """
    
    CREATE_USER_URI = '/v1_0/apiuser'

    def __init__(self, config):
        """
        Initializes the SandboxUserProvisioning class with the configuration.
        
        :param config: A dictionary containing the necessary configuration, including 'userID', 'primaryKey', 'baseURL', 
                       and 'providerCallbackHost'.
        """
        
        self.config = config

    def create(self):
        """
        Creates a new sandbox user and retrieves the API key and target environment.
        
        This method performs a series of POST and GET requests to create the sandbox user, generate an API key, and
        fetch the user's details from the API.

        :return: A dictionary with details such as 'baseURL', 'userID', 'primaryKey', 'apiKeySecret', 'targetEnvironment',
                 and 'providerCallbackHost'.
        :raises: Raises exceptions based on errors encountered during the API requests.
        """
        
        user_id = self.config['userID']
        primary_key = self.config['primaryKey']
        base_url = self.config['baseURL']

        headers = {
            "X-Reference-Id": user_id,
            "Ocp-Apim-Subscription-Key": primary_key,
            'Content-Type': 'application/json'
        }

        body = {
            'providerCallbackHost': self.config['providerCallbackHost']
        }

        response0_status, data0 = Request.request_post(base_url + self.CREATE_USER_URI, headers, body)

        if response0_status != 201:
            self.verif_exception(data0)
        else:
            headers2 = {
                "Ocp-Apim-Subscription-Key": primary_key,
                'Content-Type': 'application/json'
            }
            response1_status, data1 = Request.request_post(base_url + self.CREATE_USER_URI + f"/{user_id}/apikey", headers2)
            data1 = json.loads(data1)

            if response1_status != 201:
                self.verif_exception(data1)
            else:
                response2_status, data2 = Request.request_get(base_url + self.CREATE_USER_URI + f"/{user_id}", headers2)
                
                if response2_status == 200:
                    return {
                        'baseURL': base_url,
                        'userID': user_id,
                        'primaryKey': primary_key,
                        'apiKeySecret': data1['apiKey'],
                        'targetEnvironment': data2['targetEnvironment'],
                        'providerCallbackHost': data2['providerCallbackHost']
                    }

