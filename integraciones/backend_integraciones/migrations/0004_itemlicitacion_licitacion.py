# Generated by Django 3.1.2 on 2020-10-20 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend_integraciones', '0003_auto_20201014_0324'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemlicitacion',
            name='licitacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend_integraciones.licitacion'),
        ),
    ]
