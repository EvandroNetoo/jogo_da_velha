from django.db import models


class User(models.Model):
    usuario =  models.CharField(max_length=15)
    senha = models.CharField(max_length=50)
    
    def __str__(self):
        return self.usuario
