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
import re, datetime
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, F, Value, CharField, Sum, Count, OuterRef, Subquery, TextField, IntegerField
from django.db.models.functions import Cast
from django.utils.timezone import get_current_timezone

# -------- MODEL -----------
from polling_app.models import Master_Polling
# ----- END MODEL ------

# Create your views here.
class IndexView(View):
	def get(self, request):
		all_voting = Master_Polling.objects.get_active_polling()
		data = {
			'all_voting':all_voting,
		}
		return render(request, 'polling_app/base/home.html', data)
