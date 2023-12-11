import os
from django.db import models
from datetime import datetime
from django.core.mail import send_mail
class Dht(models.Model):
     temp = models.FloatField(null=True)
     hum = models.FloatField(null=True)
     dt = models.DateTimeField(auto_now_add=True,null=False)

     def __str__(self):
        return str(self.temp)

     def save(self, *args, **kwargs):
          if self.temp > 20:
               from app.views import sendtele,sendwhatsap
               sendtele(self)
               sendwhatsap(self)
               send_mail(
                    "Temperature Alert - Anomaly Detected in the Machine",
                    f"""
                    This is an automated alert to inform you that the temperature in the machine has exceeded the normal threshold.
                         Details:
                         - Temperature: {self.temp}
                         - Date and Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                         
                    Immediate attention is required to address this anomaly. Please investigate and take necessary actions to prevent any potential issues.
                         
                    Thank you for your prompt attention to this matter.
                         
                    Best regards,""",
                    'soptimaze@gmail.com',
                    ['moradahmaidi9@gmail.com'],
                    fail_silently=False,
               )
               return super().save(*args, **kwargs)
