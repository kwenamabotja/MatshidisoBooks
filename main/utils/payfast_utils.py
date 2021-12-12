import hashlib
import urllib

from django.conf import settings


class PayFastUtil(object):

    def __init__(self):
        """Initialising my class."""
        self.MERCHANT_ID = settings.PAYFAST_MERCHANT_ID
        self.MERCHANT_KEY = settings.PAYFAST_MERCHANT_KEY
        self.BASE_URL = settings.PAYFAST_BASE_URL

    def generate_form(self, buyer, order, amount, url=None):
        """Generate payment form."""
        data = {
            # Merchant details
            'merchant_id': self.MERCHANT_ID,
            'merchant_key': self.MERCHANT_KEY,
            'return_url': f'{url}?action=return',
            'cancel_url': f'{url}?action=cancel',
            'notify_url': f'{url}?action=notify',
            # Buyer details
            'name_first': buyer['first_name'],
            'name_last': buyer['last_name'],
            'email_address': buyer['email'],
            # Transaction details
            'm_payment_id': '1234',  # Unique payment ID to pass through to notify_url
            'amount': f"{amount}",
            'item_name': 'Order#123'
        }
        # Generate signature (see step 2)
        signature = self.generateSignature(data);
        data['signature'] = signature

        htmlForm = f'<form action="https://{self.BASE_URL}/eng/process" method="post">'
        for key in data:
            htmlForm += f'<input name="{key}" type="hidden" value="{data[key]}" />'

        htmlForm += '<input class="main-button" type="submit" value="Pay Now" /></form>'
        return htmlForm

    def generateSignature(self, dataArray, passPhrase=''):
        payload = ""
        for key in dataArray:
            # Get all the data from PayFast and prepare parameter string
            payload += key + "=" + urllib.parse.quote_plus(dataArray[key].replace("+", " ")) + "&"
        # After looping through, cut the last & or append your passphrase
        payload = payload[:-1]
        if passPhrase != '':
            payload += f"&passphrase={passPhrase}"
        return hashlib.md5(payload.encode()).hexdigest()

