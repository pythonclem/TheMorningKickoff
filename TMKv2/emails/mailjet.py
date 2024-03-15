import environ
env = environ.Env()
environ.Env.read_env("TMKv2\\TMKv2\\.env")
from django.core.management.base import BaseCommand
from mailjet_rest import Client

API_KEY = env("MAILJET_API")
API_SECRET = env("MAILJET_SECRET")

mailjet = Client(auth=(API_KEY, API_SECRET))

def sendEmail(email):
    with open('match_info.html', 'r', encoding='iso-8859-1') as file:
        html_content = file.read()
    data = {
  'FromEmail': 'c.thibault16@gmail.com',
  'FromName': 'Mailjet Pilot',
  'Subject': 'Your email flight plan!',
  'Text-part': 'Dear passenger, welcome to Mailjet! May the delivery force be with you!',
  'Html-part': html_content,
  'To': str(email),
            }
    result = mailjet.send.create(data=data)

    print(result)


class Command(BaseCommand):
    def handle(self, *args, **options):
        sendEmail()