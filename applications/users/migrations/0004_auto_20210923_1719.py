# Generated by Django 3.2.3 on 2021-09-23 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_membership_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tribes',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='users', verbose_name='Avatar Grupo'),
        ),
        migrations.AlterField(
            model_name='tribes',
            name='description',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Descripcion'),
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('group', 'user')},
        ),
    ]