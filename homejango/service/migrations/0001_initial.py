# Generated by Django 4.2.13 on 2024-06-04 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Имя')),
                ('phone', models.IntegerField(verbose_name='Телефон')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='ФИО врача')),
                ('profession', models.CharField(max_length=30, verbose_name='Профессия')),
                ('salary', models.IntegerField(verbose_name='ЗП')),
            ],
        ),
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_procedure', models.CharField(max_length=30, verbose_name='Название процедуры')),
                ('eng_name_procedure', models.CharField(max_length=30, verbose_name='Название процедуры на англ')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.IntegerField(verbose_name='Цена')),
            ],
        ),
        migrations.CreateModel(
            name='Vacations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_vacations', models.DateField(verbose_name='Дата отпуска')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Pets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=30, verbose_name='Кличка')),
                ('birthdate', models.DateField(verbose_name='Дата рождения')),
                ('breed', models.CharField(max_length=20, verbose_name='Порода')),
                ('color', models.CharField(max_length=20, verbose_name='Окрас')),
                ('clients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.clients')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_order', models.DateTimeField(verbose_name='Дата рождения')),
                ('clients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.pets')),
                ('procedure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.procedure')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='procedure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.procedure'),
        ),
    ]
