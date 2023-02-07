from django.urls import path, include, re_path
from django.urls import path, include
from django.conf.urls import url

# from . import views
from .views import base_views
from .views import polling_views
# from .views import booking_views
# from .views import busdetail_views
# from .views import master_satuan_views
from django.conf.urls import handler403

# handler403 ='onlineshop_admin.views.base_views.error_403_view' 

app_name = 'polling_app'
urlpatterns = [
	path('', base_views.IndexView.as_view(), name = 'index_main'),
	path('polling/', include([
		path('<uuid:polling_id>/', polling_views.ShowPollingViews.as_view(), name='show_polling'),
		path('createpolling/', polling_views.CreatePollingViews.as_view(), name='create_polling'),
	])),
	# path('show_result/', base_views.ShowResultView.as_view(), name = 'show_result'),

	# # ADD JOEL (11 Juni 2022 - RIZQ SANJATEK) => UPDATE TEMPLATE NEW =========================================
	# path('scan/', base_views.ScanQrCode.as_view(), name = 'scan'),
	# path('view/<str:action>/', base_views.KoleksiDetail.as_view(), name = 'koleksi_detail'),
	# path('tentang/', base_views.TentangKami.as_view(), name = 'tentang'),
	# path('penggunaan/', base_views.CaraPakaiApp.as_view(), name = 'cara_pakai'),
	# path('tips/', base_views.TipsAndTrik.as_view(), name = 'tips'),
	# path('tips/view/<str:news_id>/', base_views.TipsAndTrik_Detail.as_view(), name = 'tips_view'),
	# path('official/', base_views.OfficialViews.as_view(), name = 'official'),
]