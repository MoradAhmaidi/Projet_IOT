import csv
import telepot
from datetime import datetime

from .models import Dht
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from twilio.rest import Client



#pour afficher home page
def home(request):
    return HttpResponse('<h1>bonjour à tous</h1>')

#pour recupere data
def dht(request):
    tab = Dht.objects.all()
    s = {'tab': tab}
    return render(request, 'tables.html', s)

#pour afficher les tables
def table(request):
    derniere_ligne = Dht.objects.last()
    derniere_date = Dht.objects.last().dt
    delta_temps = timezone.now()
    difference_minutes = delta_temps.seconds // 60
    temps_ecoule = ' il y a ' + str(difference_minutes) + ' min'
    if difference_minutes> 60:
        temps_ecoule = 'il y ' + str(difference_minutes // 60) + 'h' + str(difference_minutes % 60) + 'min'
        valeurs = {'date': temps_ecoule, 'id': derniere_ligne.id, 'temp':
        derniere_ligne.temp, 'hum': derniere_ligne.hum}
    return render(request, 'value.html', {'valeurs': valeurs})

#pour tetecherge fichier csv
def download_csv(request):
    model_values = Dht.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dht.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum','dt')
    for row in liste:
        writer.writerow(row)
    return response

#pour afficher les graphes
def graphique(request):
    return render(request, 'Chart.html')
# récupérer toutes les valeur de température et humidity sous forme un #fichier json
def chart_data(request):
    dht = Dht.objects.all()

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier 24h
# et envoie sous forme JSON
def chart_data_jour(request):
    dht = Dht.objects.all()
    now = timezone.now()

    # Récupérer l'heure il y a 24 heures
    last_24_hours = now - timezone.timedelta(hours=24)

    # Récupérer tous les objets de Module créés au cours des 24 dernières heures
    dht = Dht.objects.filter(dt__range=(last_24_hours, now))
    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier semaine
# et envoie sous forme JSON
def chart_data_semaine(request):
    dht = Dht.objects.all()
    # calcul de la date de début de la semaine dernière
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=7)
    print(datetime.timedelta(days=7))
    print(date_debut_semaine)

    # filtrer les enregistrements créés depuis le début de la semaine dernière
    dht = Dht.objects.filter(dt__gte=date_debut_semaine)

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }

    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier moins
# et envoie sous forme JSON
def chart_data_mois(request):
    dht = Dht.objects.all()

    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=30)
    print(datetime.timedelta(days=30))
    print(date_debut_semaine)

    # filtrer les enregistrements créés depuis le début de la semaine dernière
    dht = Dht.objects.filter(dt__gte=date_debut_semaine)

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)

def sendtele(dht):
    token = '6436101701:AAHdYFMJXV4uFdDYoTqq1jsEhgSV1AogDMI'
    rece_id = 1092321991
    bot = telepot.Bot(token)

    message = f"""
    🚨 Temperature Alert! 🚨

The current temperature has exceeded the normal threshold.

    🌡️ Temperature: {dht.temp}
    💧 Humidity: {dht.hum}
    📅 Date and Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Anomaly detected in the machine. Immediate attention is required!

#TemperatureAlert #MachineAnomaly
    """

    bot.sendMessage(rece_id, message)
    print(bot.sendMessage(rece_id, 'OK.'))

def sendwhatsap(dht):
    account_sid = 'AC3da34e6234a1cbd00d6faaa4aa97bbd7'
    auth_token = '9146f244fc4c4c9fab4286a2a404037a'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=f"""
        🚨 Alert: High Temp & Humidity 🚨
Machine Anomaly Detected:
    🌡️ Temp: {dht.temp}
    💧 Humidity: {dht.hum}
    📅 Date & Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}""",
        to='whatsapp:+212615503124'
    )