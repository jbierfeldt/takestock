from django.core.management.base import BaseCommand, CommandError

import os
from datetime import date
from django.shortcuts import get_list_or_404
from takestock.models import Club
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import ho.pisa as pisa
import StringIO


class Command(BaseCommand):
	help = 'Gathers current stock prices from Google Finance using stock_getter script (imported) and updates all stocks in the database to reflect the current stock price.'
	
	def handle(self, *args, **options):
	
		club_list = get_list_or_404(Club)
		for club in club_list:
			for member in club.memberinstance_set.select_related():
				if member.receive_daily_emails == True:
					pdf_name_string = "{name} - {date} Report".format(name=club.name, date=date.today())
					subject_string = "{name} Daily Report".format(name=club.name)
					body_string = "What's up {member_name}? You trying to party tonight? Well, just make sure your funds are in order first. I've attached your daily stock report for {club_name}. Check it out!".format(member_name=member.member.name, club_name=club.name)
					render = render_to_string("/var/www/bierfeldt/mysite/templates/takestock/club_detail.html", { "club": club, })
					out = StringIO.StringIO()
					pdf = pisa.CreatePDF(StringIO.StringIO(render), out)
					email = EmailMessage(subject_string, body_string, 'jbierfeldt@gmail.com', [member.member.email])
					email.attach(pdf_name_string, out.getvalue(), 'application/pdf')
					email.send()
