# Generated by Django 3.2.3 on 2021-08-30 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210830_1803'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membership',
            options={'ordering': ['id'], 'verbose_name': 'Miembros', 'verbose_name_plural': 'Miembros'},
        ),
    ]