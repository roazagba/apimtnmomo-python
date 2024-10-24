import json
import os
import base64
import time
import requests

class TokenManager:
    """
    A class to manage API tokens for MTN MoMo.
    """

    def __init__(self):
        """
        Initialize the class instance.

        This constructor sets up the file path for the token file and defines the URI for token-related requests.

        :attribute token_file: The path to the token file, stored in the current module's directory.
        :attribute TOKEN_URI : The URI used for token-related API requests.
        """
        
        self.token_file = os.path.join(os.path.dirname(__file__), '/token.json')
        self.TOKEN_URI = "/token/"

    def get_token(self, config, product):
        """
        Retrieves the access token.

        Checks if a valid token exists. If not, fetches a new token.

        :param config: The configuration object for retrieving API credentials.
        :param product: The product or service name for which the token is requested.
        :return: The access token.
        :raises Exception: If fetching the token fails.
        """
        
        token_data = self.load_token()

        if token_data and self.is_token_valid(token_data):
            return token_data['access_token']
        else:
            new_token_data = self.fetch_new_token(config, product)
            self.save_token(new_token_data)
            return new_token_data['access_token']

    def is_token_valid(self, token_data):
        """
        Checks if the token is still valid.

        :param token_data: The token data dictionary containing the token and expiration time.
        :return: True if the token is valid, False otherwise.
        """
        
        return 'expires_at' in token_data and time.time() < token_data['expires_at']

    def fetch_new_token(self, config, product):
        """
        Fetches a new access token.

        :param config: The configuration object for retrieving API credentials.
        :param product: The product or service name for which the token is requested.
        :return: The new token data, including the token and expiration time.
        :raises Exception: If the request fails with an unauthorized or server error.
        """
        
        url = f"{config.retrieve_value(product, 'host')}{product}{self.TOKEN_URI}"
        primary_key = config.retrieve_value(product, 'PrimaryKey')
        api_key_secret = config.retrieve_value(product, 'ApiKeySecret')
        user_id = config.retrieve_value(product, 'userId')

        headers = {
            "Authorization": f"Basic {base64.b64encode(f'{user_id}:{api_key_secret}'.encode()).decode()}",
            "Ocp-Apim-Subscription-Key": primary_key,
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers)

        if response.status_code != 200:
            if response.status_code == 401:
                raise Exception(f"Unauthorized: {response.json().get('error', 'Unknown error')}")
            elif response.status_code == 500:
                raise Exception(response.json().get('error', 'Unknown server error'))
            else:
                raise Exception("Another error occurred")

        token_data = response.json()
        token_data['expires_at'] = time.time() + 3600  # Token expires in 1 hour

        return token_data

    def save_token(self, token_data):
        """
        Saves the token data to a file.

        :param token_data: The token data to save.
        """
        with open(self.token_file, 'w') as f:
            json.dump(token_data, f)

    def load_token(self):
        """
        Loads the token data from a file.

        :return: The token data dictionary, or None if the file does not exist.
        """
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as f:
                return json.load(f)
        return None
