from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    PERFIL_USUARIO_CHOICES = (
        ('CHEFE', 'Chefe de Gabinete'),
        ('ASSESSOR', 'Assessor'),
        ('ATENDENTE', 'Atendente'),
        ('CONSULTA', 'Consulta'),
    )
    perfil = models.CharField(max_length=20, choices=PERFIL_USUARIO_CHOICES, blank=True, null=True, default=None, verbose_name='Perfil do Usuário')
    telefone = models.CharField(max_length=20, blank=True)
    cargo = models.CharField(max_length=100, blank=True)
    
    def save(self, *args, **kwargs):
        self.is_active = bool(self.perfil)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username