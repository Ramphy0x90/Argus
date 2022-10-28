from django.conf import settings
import requests

class Zoho:
    def __init__(self):
        # Get env variables
        self.env = settings.ENV


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Zoho, cls).__new__(cls)
        return cls.instance


    def __get_token(self):
        # Set request headers
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        # Set request URL params
        params = {
            'refresh_token': self.env('ZOHO_REFRESH_TOKEN'),
            'client_id': self.env('ZOHO_CLIENT_ID'),
            'client_secret': self.env('ZOHO_CLIENT_SECRET'),
            'scope': self.env('ZOHO_SCOPE'),
            'grant_type': self.env('ZOHO_GRANT_TYPE')
        }
        # Send token request
        token_request = requests.post(self.env('ZOHO_API_URL'), params = params, headers = headers)
        # Extracting data in json format
        data = token_request.json()

        return data['access_token'] if ('access_token' in data) else False 


    def get_ticket(self, id):
        # Get token
        token = self.__get_token()
        # Set request headers
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'orgId': self.env('ORGANIZATION_ID'),
            'Authorization': 'Zoho-oauthtoken %s' % token 
        }
        # Check if token and id exists
        if token and id:
            # Send ticket request
            ticket_request = requests.post('https://desk.zoho.eu/api/v1/tickets/%s' % id, headers = headers)
            # Extracting data in json format
            data = ticket_request.json()

            return data

        return False