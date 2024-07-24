from django.db import models
from django.core.exceptions import ValidationError
import re
from custom_user.models import CustomUser

class Cartao(models.Model):
    numero = models.CharField(max_length=30)
    lote = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero

    def clean(self):
        if not re.match(r'^\d{16}$', self.numero):
            raise ValidationError('O número do cartão deve conter 16 dígitos.')
        if not self.lote:
            raise ValidationError('O lote não pode estar vazio.')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cartão'
        verbose_name_plural = 'Cartões'
        db_table = 'cartao'
        indexes = [
            models.Index(fields=['numero']),
        ]


class LoteCartoes(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    nome = models.CharField(max_length=30, blank=True)
    data = models.CharField(max_length=8, blank=True)
    numero = models.CharField(max_length=8, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Lote de Cartões (Número: {self.numero})'

    def clean(self):
        if self.quantidade <= 0:
            raise ValidationError('A quantidade deve ser um número positivo.')
        if self.data and not re.match(r'^\d{2}-\d{2}-\d{4}$', self.data):
            raise ValidationError('A data deve estar no formato dd-mm-aaaa.')
        if self.numero and not re.match(r'^\d{8}$', self.numero):
            raise ValidationError('O número do lote deve conter 8 dígitos.')

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Lote de Cartões'
        verbose_name_plural = 'Lotes de Cartões'
        db_table = 'lote_cartoes'