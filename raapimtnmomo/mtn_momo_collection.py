from .mtn_momo import MTNMoMo
from .utilities import Helpers
from .requestss import *
from .exceptions import *
from .token_manager import TokenManager

class MTNMoMoCollection(MTNMoMo):
    """
    MTNMoMoCollection is a subclass of MTNMoMo that handles MoMo Collection API operations,
    such as creating transactions, retrieving account balances, and getting basic user info.
    """
    
    product = 'collection'

    REQUEST_TO_PAY_URI = '/v1_0/requesttopay'
    ACCOUNT_BALANCE_URI = '/v1_0/account/balance'
    GET_BASIC_USER_INFO_URI = '/v1_0/accountholder'

    def get_url(self) -> str:
        """
        Constructs the base URL for the MTN MoMo Collection API by appending the product to the host.

        :return: Full URL as a string.
        """
        
        return f"{self.config.host}{self.product}"

    def create_transaction(self, params, custom_params=None):
        """
        Creates a new payment transaction with the required parameters.
        
        :param params: A dictionary containing transaction details such as amount, referenceExternalID, numberMoMo, etc.
        :param custom_params: Optional custom parameters for the transaction.
        :return: A dictionary containing the transaction ID and any custom parameters.
        :raises ValueError: If any required parameter is missing.
        """
        
        required_keys = ['amount', 'referenceExternalID', 'numberMoMo', 'description', 'note']
        missing_keys = [key for key in required_keys if key not in params]

        if missing_keys:
            raise ValueError(f"The missing keys are: {', '.join(missing_keys)}")

        currency = self.config.currency
        access_token = self.get_token()
        x_reference_id = Helpers.uuid4()
        primary_key = self.config.collection['primary_key']
        target = self.config.target

        headers = {
            "Ocp-Apim-Subscription-Key": primary_key,
            "X-Reference-Id": x_reference_id,
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": target,
            'Content-Type': 'application/json'
        }

        body = {
            'amount': params['amount'],
            'currency': currency,
            'externalId': params['referenceExternalID'],
            'payer': {
                "partyIdType": "MSISDN",
                "partyId": params['numberMoMo']
            },
            "payerMessage": params['description'],
            "payeeNote": params['note']
        }

        response = Request.request_post(self.get_url() + self.REQUEST_TO_PAY_URI, headers, body)

        if response[0] != 202:
            self.verif_exception(response)

        return {'transactionId': x_reference_id, 'customParams': custom_params}

    def get_token(self):
        """
        Retrieves the access token using the TokenManager.

        :return: The access token as a string.
        """
        
        token_manager = TokenManager()
        return token_manager.get_token(self.config, self.product)

    def get_transaction(self, x_reference_id):
        """
        Retrieves the details of a specific transaction based on its reference ID.

        :param x_reference_id: The reference ID of the transaction.
        :return: The transaction details as a dictionary.
        :raises ValueError: If the transaction reference ID is invalid.
        """
        
        if not x_reference_id:
            raise ValueError("Transaction reference ID is invalid")

        access_token = self.get_token()
        primary_key = self.config.collection['primary_key']
        target = self.config.target

        headers = {
            "Ocp-Apim-Subscription-Key": primary_key,
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": target,
            'Content-Type': 'application/json'
        }

        response = Request.request_get(f"{self.get_url()}{self.REQUEST_TO_PAY_URI}/{x_reference_id}", headers)

        if response[0] != 200:
            self.verif_exception(response)

        return response[1]

    def get_account_balance(self, currency=None):
        """
        Retrieves the account balance.

        :param currency: Optional. The currency for which to retrieve the balance.
        :return: The account balance as a dictionary.
        """
        
        access_token = self.get_token()
        primary_key = self.config.collection['primary_key']
        target = self.config.target

        headers = {
            "Ocp-Apim-Subscription-Key": primary_key,
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": target,
            'Content-Type': 'application/json'
        }

        url = f"{self.get_url()}{self.ACCOUNT_BALANCE_URI}"
        if currency:
            url += f"/{currency}"

        response = Request.request_get(url, headers)

        if response[0] != 200:
            self.verif_exception(response)

        return response[1]

    def get_basic_user_info(self, number_momo):
        """
        Retrieves basic user information based on the MoMo number.

        :param number_momo: The MoMo number to query.
        :return: The basic user information as a dictionary.
        """
        
        access_token = self.get_token()
        primary_key = self.config.collection['primary_key']
        target = self.config.target

        headers = {
            "Ocp-Apim-Subscription-Key": primary_key,
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": target,
            'Content-Type': 'application/json'
        }

        url = f"{self.get_url()}{self.GET_BASIC_USER_INFO_URI}/MSISDN/{number_momo}/basicuserinfo"

        response = Request.request_get(url, headers)

        if response[0] != 200:
            self.verif_exception(response)

        return response[1]
