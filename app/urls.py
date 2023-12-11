from django.urls import path
from . import views
from . import api
urlpatterns = [
  path('',views.home,name='home'),
  path('data',views.dht,name='data'),
  path('api',api.dhtser,name='json'),
  path('chart',views.graphique,name='chart'),
  path('chart-data',views.chart_data, name='chart-data'),
  path('chart-data-jour',views.chart_data_jour,name='chart-data-jour'),
  path('chart-data-mois',views.chart_data_mois, name='chart-data-mois'),
  path('chart-data-semaine',views.chart_data_semaine,name='chart-data-semaine'),
  path('download_csv',views.download_csv, name='download_csv'),
]
