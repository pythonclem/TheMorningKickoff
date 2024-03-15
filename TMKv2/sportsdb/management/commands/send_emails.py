from emails.email_sender import sendEmails
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        sendEmails()
