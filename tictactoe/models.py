from django.db import models
import secrets
from autenticacao.models import User    


class Room(models.Model):
    dono = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    code = models.CharField(max_length=16)
    
    privada = models.BooleanField(default=False)
    senha = models.CharField(blank=True, max_length=20)

    tabuleiro = models.JSONField(default=[[" " for col in range(3)] for row in range(3)])
    jogadores = models.JSONField(default=[])
    turno = models.IntegerField(default=0)
    
    vencedor = models.IntegerField(null=True, default=None)
    
    def generate_token(self):
        token = secrets.token_bytes(8).hex()
        if Room.objects.filter(code=token).exists():
            self.generate_token(self)
        return token
    
    def troca_turno(self):
        self.turno = 0 if self.turno == 1 else 1

    def save(self, *args, **kwargs):
        if not self.code: 
            self.code = self.generate_token()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.code