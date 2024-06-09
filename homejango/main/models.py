from django.db import models

# Create your models here.


class Reviews(models.Model):
    name = models.CharField('Название отзыва', max_length=30)
    description = models.TextField('Текст отзыва')
