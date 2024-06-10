from django.db import models

# Create your models here.


class Reviews(models.Model):
    name = models.CharField('Название отзыва', max_length=30)
    description = models.TextField('Текст отзыва')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отзывы/Reviews'
        verbose_name_plural = 'Отзывы/Reviews'