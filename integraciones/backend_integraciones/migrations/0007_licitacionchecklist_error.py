# Generated by Django 3.1.2 on 2020-10-27 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_integraciones', '0006_procesoextraccion_historico'),
    ]

    operations = [
        migrations.AddField(
            model_name='licitacionchecklist',
            name='error',
            field=models.BooleanField(default=False),
        ),
    ]
