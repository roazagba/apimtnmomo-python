import requests

class Request:
    """
    A utility class for making HTTP GET and POST requests.
    """
    
    @staticmethod
    def request_post(url, headers, body=None):
        """
        Sends a POST request to the specified URL with the provided headers and optional body.
        
        :param url: The target URL for the POST request.
        :param headers: A dictionary of HTTP headers to include in the request.
        :param body: An optional JSON payload to send with the request.
        :return: A tuple containing the status code and the response data (JSON or text based on Content-Type).
        """
        
        response = requests.post(url, headers=headers, json=body)
        
        if response.headers.get('Content-Type') == 'application/json':
            return response.status_code, response.json()
        else:
            return response.status_code, response.text

    @staticmethod
    def request_get(url, headers):
        """
        Sends a GET request to the specified URL with the provided headers.
        
        :param url: The target URL for the GET request.
        :param headers: A dictionary of HTTP headers to include in the request.
        :return: A tuple containing the status code and the JSON response data.
        """
        
        response = requests.get(url, headers=headers)
        return response.status_code, response.json()
