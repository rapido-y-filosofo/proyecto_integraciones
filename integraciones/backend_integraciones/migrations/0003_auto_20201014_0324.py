# Generated by Django 3.1.2 on 2020-10-14 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend_integraciones', '0002_auto_20201014_0317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licitacion',
            name='comprador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_integraciones.personaorganismo'),
        ),
    ]