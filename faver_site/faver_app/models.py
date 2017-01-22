from django.db import models

# Create your models here.
class FaverUser(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32, default="")
    coins = models.IntegerField(default=5)
    reputation = models.IntegerField(default=10)

class FaverRequest(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    issuer = models.ForeignKey('FaverUser', default=True)
    reward = models.IntegerField(default=10)
    latitude = models.DecimalField(max_digits=6, decimal_places=3, default=43.663)
    longitude = models.DecimalField(max_digits=6, decimal_places=3, default=-79.396)

class FaverContract(models.Model):
    request = models.ForeignKey('FaverRequest', default=True, related_name='request')
    issuer = models.ForeignKey('FaverUser', default=True, related_name='issuer')
    acceptor = models.ForeignKey('FaverUser', default=True, related_name='acceptor')
