import requests
import json

class APIErrorException(Exception):
    #"""API error exception when API return error in payload"""
    def __init__(self, error_type, error_description):
        self.type = error_type
        self.description = error_description
        super().__init__(f"{error_type}: {error_description}")


class API:
    def __init__(self, url=None):
        self.url = url   
    
    def send_get_request(self, data):
        
        response = requests.get(self.url, data)
        
        # Check if the response contains JSON
        if response.headers['content-type'] == 'application/json':
            payload = response.json()
            # Check if 'error' is in the JSON payload from the server
            if 'error' in payload:
                raise APIErrorException(payload['error']['type'], payload['error']['description'])

        if response.status_code == 200:
            payload = response.json()
            return payload  # Returns the payload as a Python dictionary
        else:
            # The request failed; raise an HTTP exception
            response.raise_for_status()
