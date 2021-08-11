# Generated by Django 3.2.3 on 2021-07-14 16:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210714_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tribes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, unique=True, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, max_length=400, null=True, verbose_name='Descripcion')),
                ('user', models.PositiveIntegerField(blank=True, verbose_name='Creado por')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Administrar Grupos',
                'verbose_name_plural': 'Administrar Grupos',
                'ordering': ['name'],
            },
        ),
        migrations.RemoveField(
            model_name='user',
            name='tribe',
        ),
        migrations.DeleteModel(
            name='UserGroups',
        ),
        migrations.AddField(
            model_name='tribes',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='members', to=settings.AUTH_USER_MODEL),
        ),
    ]
