from datetime import date
import os
import StringIO

from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_list_or_404
from django.template.loader import render_to_string
import ho.pisa as pisa

from takestock.models import Club


BODY = "What's up {member}? You trying to party tonight? Well, just make " \
    "sure your funds are in order first. I've attached your daily stock " \
    'report for {club}. Check it out!'
# TODO(jds): Fix this. Shouldn't need an absolute path.
TEMPLATE = '/var/www/bierfeldt/mysite/templates/takestock/club_detail.html'


class Command(BaseCommand):
    help = 'Gathers current stock prices from Google Finance using ' \
        'stock_getter script (imported) and updates all stocks in the ' \
        'database to reflect the current stock price.'
    
    def handle(self, *args, **options):
    
        club_list = get_list_or_404(Club)
        for club in club_list:
            for member in club.memberinstance_set.select_related():
                if member.receive_daily_emails == True:
                    name = "{name} - {date} Report".format(name=club.name,
                                                           date=date.today())
                    subject = "{name} Daily Report".format(name=club.name)
                    body = BODY.format(member=member.member.name,
                                       club=club.name)
                    render = render_to_string(TEMPLATE, {"club": club})
                    out = StringIO.StringIO()
                    pdf = pisa.CreatePDF(StringIO.StringIO(render), out)
                    email = EmailMessage(subject, body, 'jbierfeldt@gmail.com',
                                         [member.member.email])
                    email.attach(name, out.getvalue(), 'application/pdf')
                    email.send()
