import os

class MTNMoMoConfig:
    """
    Configuration class for MTN MoMo API.
    
    This class is responsible for loading the environment variables necessary
    for interacting with the MTN MoMo API, including credentials, host URLs,
    and API keys.
    """
    
    def __init__(self):
        """
        Initializes the configuration by loading environment variables or
        setting default values. 
        
        Environment variables:
            - RA_BASE_URL: The base URL of the MTN MoMo API.
            - RA_CURRENCY: The default currency for transactions (default: EUR).
            - RA_TARGET_ENVIRONMENT: Target environment (default: sandbox).
            - RA_CALLBACK_URL: Callback URL for asynchronous notifications.
            - RA_COLLECTION_API_KEY_SECRET: The API key secret for the collection service.
            - RA_COLLECTION_PRIMARY_KEY: The primary subscription key for the collection service.
            - RA_COLLECTION_USER_ID: The user ID for the collection service.
        
        If the environment variables are not found, default values will be used.
        """
        
        self.host = os.getenv('RA_BASE_URL', 'https://sandbox.momodeveloper.mtn.com/')
        self.currency = os.getenv('RA_CURRENCY', 'EUR')
        self.target = os.getenv('RA_TARGET_ENVIRONMENT', 'sandbox')
        self.callback_url = os.getenv('RA_CALLBACK_URL', 'http://localhost:8000')
        
        self.collection = {
            'api_key_secret': os.getenv('RA_COLLECTION_API_KEY_SECRET', 'df7c71c3c5ac4d3e9433daf43a6e2987'),
            'primary_key': os.getenv('RA_COLLECTION_PRIMARY_KEY', '57ca5f1907074bf590090041688d781d'),
            'user_id': os.getenv('RA_COLLECTION_USER_ID', 'd9097d11-90f4-411c-8c28-b2f97ad7ef61')
        }
        
        self.config = {
            'host': self.host,
            'currency': self.currency,
            'target': self.target,

            'callbackUrl': self.callback_url,
            'collectionApiKeySecret': self.collection['api_key_secret'],
            'collectionPrimaryKey': self.collection['primary_key'],
            'collectionUserId': self.collection['user_id']
        }
        
    def retrieve_value(self, product: str = "", config_key: str = ""):
        """
        Retrieves a specific configuration value based on the product and key provided.
        
        Args:
            product (str): The product type (e.g., 'collection') which can be used
                           to prefix the configuration keys. Defaults to an empty string.
            config_key (str): The specific configuration key to retrieve.
        
        Returns:
            str: The value associated with the given product and configuration key.
        
        Raises:
            Exception: If the requested key does not exist in the configuration.
        """
        
        filtered_nocoll = [key for key in self.config.keys() if not key.startswith(product)]

        key = config_key if config_key in filtered_nocoll else f"{product.lower()}{config_key[0].upper()}{config_key[1:]}"

        if key not in self.config:
            raise Exception(f"{key} does not exist in config credentials")

        return self.config[key]
