from django.db import models
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group


class Norms:
     MIN_TEMP = -2
     MAX_TEMP = 4
     MIN_HUM = 30
     MAX_HUM = 50

class TemplateMessage:
     EMAIL = '''
     🚨 Alert: High Temp & Humidity 🚨
     
     The current temperature or Humidity has exceeded the normal threshold.
        Machine Anomaly Detected:
        🌡️ Temp: {temp}
        💧 Humidity: {hum}
        📅 Date and Time: {dt}
     Anomaly detected in the machine. Immediate attention is required!
    '''
     TELEGRAM = '''
     🚨 Alert: High Temp & Humidity 🚨
     
     The current temperature or Humidity has exceeded the normal threshold.
        Machine Anomaly Detected:
        🌡️ Temp: {temp}
        💧 Humidity: {hum}
        📅 Date and Time: {dt}
     Anomaly detected in the machine. Immediate attention is required!
     '''
     WHATSAPP = '''
     🚨 Alert: High Temp & Humidity 🚨
        Machine Anomaly Detected:
        🌡️ Temp: {temp}
        💧 Humidity: {hum}
        📅 Date and Time: {dt}
      Anomaly detected in the machine. Immediate attention is required!
     '''

class Dht(models.Model):
     temp = models.FloatField(null=True)
     hum = models.FloatField(null=True)
     dt = models.DateTimeField(auto_now_add=True,null=False)
     CPT=0

     def __str__(self):
        return str(self.temp)

     def save(self, *args, **kwargs):
          users = User.objects.all()
          if not Norms.MIN_TEMP <= self.temp <= Norms.MAX_TEMP or Norms.MIN_HUM <= self.hum <= Norms.MAX_HUM:
               self.CPT+=1
               if self.CPT > 3:
                    from app.views import sendwhatsap,sendtele
                    '''sendwhatsap(body=TemplateMessage.WHATSAPP.format(
                         temp=self.temp,
                         hum=self.hum,
                         dt=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ))'''
               from app.views import sendtele
               sendtele(message=TemplateMessage.TELEGRAM.format(
                    temp=self.temp,
                    hum=self.hum,
                    dt=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               ))
               send_mail("Temperature Alert - Anomaly Detected in the Machine",
                    TemplateMessage.EMAIL.format(
                    temp=self.temp,
                    hum=self.hum,
                    dt=datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    'soptimaze@gmail.com',
                    [user.email for user in User.objects.all()],
                    fail_silently=False,
               )
          return super().save(*args, **kwargs)