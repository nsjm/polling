from django.conf import settings

def context_processors_function(request):
	data = {
		'app_title':settings.APP_TITLE,
	}
	return data