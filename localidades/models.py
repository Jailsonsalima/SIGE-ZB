from django.db import models

# Create your models here.

class Distrito(models.Model):
    sigla = models.CharField(max_length=10)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.sigla} - {self.nome}"
    

class Bairro(models.Model):
    distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT, related_name='bairros')
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome