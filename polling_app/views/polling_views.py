from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import requests, json, uuid, qrcode
from django.contrib.auth import login, authenticate
import re, datetime, locale
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, F, Value, CharField, Sum, Count, OuterRef, Subquery, TextField, IntegerField
from django.db.models.functions import Cast
from django.utils.timezone import get_current_timezone

# -------- MODEL -----------
from polling_app.models import Master_User, Master_Polling
# ----- END MODEL ------

class VoterValidations():
	user_detail = False
	def get_ip(self):
		user_ip = ''
		try:
			user_ip = requests.get("https://api.ipify.org/").text
		except Exception as e:
			pass
		return user_ip

def convert_to_tgl_db(date, date_format, db='postgres', use_locale = False, locale_detail='id_ID'):
	convert_result = False

	if use_locale:
		locale.setlocale(locale.LC_TIME, locale_detail)
		print(use_locale)

	if db == 'postgres':
		try:
			convert_result = datetime.datetime.strptime(date, date_format).strftime('%Y-%m-%d %I:%M:%S')
		except Exception as e:
			print('[ERROR CONVERTING DATE TO POSTGRES DATABASE]', e)
	return convert_result

class CreatePollingViews(View):
	def get(self, request):
		# GET screensize, color depth, user timezone

		data = {}
		return render(request, 'polling_app/polling/create_polling.html', data)

	def post(self, request):
		frm_question = request.POST.get('frm_question')
		frm_choices = request.POST.getlist('frm_choices[]')
		frm_allow_multiple = request.POST.get('frm_allow_multiple', False)
		frm_comment_off = request.POST.get('frm_comment_off', False)
		frm_exp_date = request.POST.get('frm_exp_date')

		if len(frm_choices) < 2:
			messages.error(request, 'Jumlah pilihan minimal 2')
			return redirect('polling_app:create_polling')
		else:
			frm_choices_fix = []
			for x in frm_choices:
				frm_choices_fix.append({'value':x})

		if frm_exp_date:
			exp_date = convert_to_tgl_db(date = frm_exp_date, date_format = '%d %B %Y %H:%M', use_locale=True)
		else:
			exp_date = None

		try:
			if request.user.is_authenticated:
				polling_creator = request.user
			else:
				polling_creator = None

			dt_polling = Master_Polling(
							polling_question = frm_question,
							polling_choices = frm_choices_fix,
							polling_allow_multiple = frm_allow_multiple,
							polling_comment_off = frm_comment_off,
							polling_exp_date = exp_date,
							polling_creator = polling_creator
						)
			dt_polling.save()
			return redirect(reverse('polling_app:show_polling', args=[dt_polling.polling_id]))
		except Exception as e:
			print('[ERROR CREATE POLLING]', e)
			messages.error(request, 'Kesalahan server, cobalah beberapa saat lagi')
			return redirect('polling_app:create_polling')

class ShowPollingViews(View):
	def get(self, request, polling_id):
		
		return HttpResponse(f'ini polling {polling_id}')
