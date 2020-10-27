# Generated by Django 3.1.2 on 2020-10-14 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdjudicacionItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField()),
                ('monto_unitario', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_origen', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoLicitacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_origen', models.IntegerField()),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_producto', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=250)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend_integraciones.categoriaitem')),
            ],
        ),
        migrations.CreateModel(
            name='Moneda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abreviatura', models.CharField(max_length=5)),
                ('nombre', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Organismo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_origen', models.CharField(max_length=30)),
                ('rut_organismo', models.CharField(max_length=30)),
                ('nombre', models.CharField(max_length=250)),
                ('cantidad_reclamos', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=30)),
                ('nombre', models.CharField(max_length=250)),
                ('contacto', models.CharField(blank=True, max_length=250, null=True)),
                ('codigo_origen', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='TipoLicitacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_origen', models.IntegerField()),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UnidadOrganismo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut_unidad', models.CharField(max_length=30)),
                ('codigo_unidad', models.CharField(max_length=120)),
                ('nombre', models.CharField(max_length=250)),
                ('direccion', models.CharField(max_length=250)),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_integraciones.comuna')),
                ('organismo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_integraciones.organismo')),
            ],
        ),
        migrations.CreateModel(
            name='PersonaOrganismo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=250, null=True)),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_integraciones.cargo')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_integraciones.persona')),
                ('unidad_organismo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_integraciones.unidadorganismo')),
            ],
        ),
        migrations.CreateModel(
            name='Licitacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=50)),
                ('nombre', models.CharField(blank=True, max_length=250, null=True)),
                ('descripcion', models.TextField()),
                ('fecha_cierre', models.DateTimeField(null=True)),
                ('etapas', models.IntegerField()),
                ('fecha_creacion', models.DateTimeField(null=True)),
                ('fecha_inicio', models.DateTimeField(null=True)),
                ('fecha_final', models.DateTimeField(null=True)),
                ('fecha_pub_respuestas', models.DateTimeField(null=True)),
                ('fecha_acto_apertura_tecnica', models.DateTimeField(null=True)),
                ('fecha_acto_apertura_economica', models.DateTimeField(null=True)),
                ('fecha_publicacion', models.DateTimeField(null=True)),
                ('fecha_adjudicacion', models.DateTimeField(null=True)),
                ('fecha_estimada_adjudicacion', models.DateTimeField(null=True)),
                ('fecha_soporte_fisico', models.DateTimeField(null=True)),
                ('fecha_tiempo_evaluacion', models.DateTimeField(null=True)),
                ('fecha_estimada_firma', models.DateTimeField(null=True)),
                ('fechas_usuario', models.DateTimeField(null=True)),
                ('fecha_visita_terreno', models.DateTimeField(null=True)),
                ('fecha_entrega_antecedentes', models.DateTimeField(null=True)),
                ('url_acta_adjudicacion', models.CharField(blank=True, max_length=250, null=True)),
                ('comprador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_integraciones.organismo')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_integraciones.estadolicitacion')),
                ('moneda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_integraciones.moneda')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_integraciones.tipolicitacion')),
            ],
        ),
        migrations.CreateModel(
            name='ItemLicitacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correlativo', models.IntegerField()),
                ('unidad_medida', models.CharField(max_length=50)),
                ('cantidad', models.FloatField()),
                ('descripcion', models.TextField()),
                ('adjudicacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend_integraciones.adjudicacionitem')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_integraciones.item')),
            ],
        ),
        migrations.AddField(
            model_name='comuna',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_integraciones.region'),
        ),
        migrations.AddField(
            model_name='adjudicacionitem',
            name='organismo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_integraciones.organismo'),
        ),
    ]
