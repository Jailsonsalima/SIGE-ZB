from django.db import models

# Create your models here.
from localidades.models import Bairro

class Lideranca(models.Model):

    TIPO_RESIDENCIA = [
        ('ALUGADA', 'Alugada'),
        ('PROPRIA', 'Própria'),
        ('CEDIDA', 'Cedida'),
        ('OUTROS', 'Outros'),
    ]

    nome_completo = models.CharField(max_length=200, verbose_name='Nome Completo')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    data_admissao = models.DateField(verbose_name='Data de Admissão')
    data_desligamento = models.DateField(null=True, blank=True, verbose_name='Data de Desligamento')
    endereco = models.CharField(max_length=255, verbose_name='Endereço')
    bairro = models.ForeignKey(Bairro, on_delete=models.PROTECT, verbose_name='Bairro')
    #distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT)
    contato_telefonico = models.CharField(max_length=20, verbose_name='Contato Telefônico')
    lotacao = models.CharField(max_length=100, verbose_name='Lotação')
    cargo = models.CharField(max_length=100, verbose_name='Cargo')
    formacao = models.CharField(max_length=150, verbose_name='Formação')
    qtd_pessoas_maior_16 = models.PositiveIntegerField(verbose_name='Qtd Pessoas Maior de 16 Anos')
    tipo_residencia = models.CharField(max_length=20, choices=TIPO_RESIDENCIA, verbose_name='Tipo de Residência')
    instagram = models.CharField(max_length=100, blank=True, verbose_name='Instagram')
    indicacao = models.CharField(max_length=200, blank=True, help_text='Quem indicou a liderança')
    titulo_eleitor = models.CharField(max_length=20, verbose_name='Título do Eleitor')
    secao_eleitoral = models.CharField(max_length=10, verbose_name='Seção Eleitoral')
    zona_eleitoral = models.CharField(max_length=10, verbose_name='Zona Eleitoral')
    local_votacao = models.CharField(max_length=200, verbose_name='Local de Votação')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    def __str__(self):
        return self.nome_completo