from django.conf import settings
from django.utils import timezone
from django.db.models.functions import ExtractMinute
from ..models import ZohoToken
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
        # Get existing token
        existing_token = ZohoToken.objects.all()
        now_time = timezone.now()

        if existing_token.count() > 0 and (now_time - existing_token.values()[0]['creation']).total_seconds() / 60 <= 5:
            return existing_token.values()[0]['token']
        else:
            # Send token request
            token_request = requests.post(self.env('ZOHO_API_URL'), params = params, headers = headers)
            # Extracting data in json format
            data = token_request.json()
            if 'access_token' in data:
                if existing_token.count() == 0:
                    new_token = ZohoToken(token = data['access_token'])
                    new_token.save()
                else:
                    existing_token.update(token = data['access_token'], creation = timezone.now())
                return data['access_token']

        return False


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
            # Url request
            url_request = 'https://desk.zoho.eu/api/v1/tickets/%s' % id
            # Send ticket request
            ticket_request = requests.get(url_request, headers = headers)
            # Extracting data in json format
            data = ticket_request.json()

            return data

        return False