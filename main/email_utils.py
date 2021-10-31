import json
import logging

from bellabooks.settings import SENDGRID_TOKEN, SENDGRID_URL

logger = logging.getLogger(__name__)


class EmailUtil(object):

    def __init__(self):
        pass

    def send_contact_email(self, contact):
        try:
            headers = {
                "Authorization": f"Bearer {SENDGRID_TOKEN}",
                "Content-Type": "application/json"
            }
            data = {
                "personalizations": [
                    {
                        "to": [{"email": "ptchankue@gmail.com"}]
                    }
                ],
                "from": {"email": "Bella Books <ptchankue@gmail.com>"},
                "subject": f"Bella Books Contact Form: {contact.email}",

                "content": [
                    {
                        "type": "text/plain",
                        "value": "Test test test!"
                    },
                    {
                        "type": "text/html",
                        "value": f"""
                    <html>
                        <head>
                            <title>Bella Books Contact Form</title>
                        </head>
                        <body>
                            <h1>Contact Added!</h1>
                            <table>
                            <tr><td>Email</td><td>Mobile number</td><td>Name</td></tr>
                            <tr><td>{contact.email}</td><td>{contact.mobile_number}r</td>
                            <td>{contact.name}</td></tr>
                            </table>
                            <h2>Message</h2>
                            <p>{contact.message}</p>
                        </body>
                    </html>
                    """
                    }
                ]
            }
            r = requests.post(url=SENDGRID_URL,
                              headers=headers,
                              data=json.dumps(data))
        except Exception as e:
            logger.error(e)