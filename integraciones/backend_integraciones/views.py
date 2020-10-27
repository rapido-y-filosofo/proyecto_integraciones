from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .api_mercado_publico import api_mercado_publico
from datetime import datetime

import time
import numpy as np
import pandas as pd

from .models import Organismo, UnidadOrganismo, PersonaOrganismo, Persona, Cargo, Comuna, Region
from .models import EstadoLicitacion, TipoLicitacion, Licitacion, Item, ItemLicitacion, CategoriaItem, AdjudicacionItem

import unidecode


def test_api_mercado_publico(request):
    api = api_mercado_publico.ApiMercadoPublico()

    fecha_inicio = '18-10-2019'

    licitaciones = api.get_licitaciones_por_fecha(
        fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y')
    )

    columnas = ['codigo_error']
    dd = pd.DataFrame(columns=columnas)
    i = 0
    total_licitaciones = licitaciones['Cantidad']
    for codigo_licitacion in licitaciones['Listado']:
        # if i == 20:
        #     break
        try:
            codigo = codigo_licitacion['CodigoExterno']
            time.sleep(2)
            licitacion_completa = api.get_licitacion_por_codigo(codigo)['Listado'][0]
            #proceso "void" que inserta en la BD, mediante el ORM de Django
            extractor(licitacion_completa)
        except Exception as e:
            print(e)
            dd = dd.append({ 'codigo_error': codigo }, ignore_index=True)
        print("###################################")
        i += 1
        print("procesada: ", i)
        print("total: {0}/{1}".format(i, total_licitaciones), " -> ", (i*1.0)/total_licitaciones)
        print("###################################")
    dd.to_excel('/home/ronofri/Escritorio/licitaciones_con_error.xlsx')

    return JsonResponse(
        {}
    )

def extractor(json_licitacion):
    diccionario = generar_diccionario()
    try:
        comprador = json_licitacion['Comprador']
        #agregar normalizador de strings!!!
        if not entidad_existe('organismo_codigo', comprador['CodigoOrganismo'], diccionario):
            organismo = Organismo(
                codigo_origen = comprador['CodigoOrganismo'],
                rut_organismo = '',
                nombre = normalizar_texto(comprador['NombreOrganismo']),
                cantidad_reclamos = json_licitacion['CantidadReclamos'],
            )

            organismo.save()

            organismo_id = organismo.id
            diccionario['organismo_codigo'][comprador['CodigoOrganismo']] = organismo_id
        else:
            organismo_id = diccionario['organismo_codigo'][comprador['CodigoOrganismo']]
        
        if not entidad_existe('region', normalizar_texto(comprador['RegionUnidad']), diccionario):
            region = Region(
                nombre = normalizar_texto(comprador['RegionUnidad']),
            )

            region.save()

            region_id = region.id
            diccionario['region'][normalizar_texto(comprador['RegionUnidad'])] = region_id

        else:
            region_id = diccionario['region'][normalizar_texto(comprador['RegionUnidad'])]
        
        if not entidad_existe('comuna', normalizar_texto(comprador['ComunaUnidad']), diccionario):
            comuna = Comuna(
                nombre = normalizar_texto(comprador['ComunaUnidad']),
                region_id = region_id,
            )

            comuna.save()

            comuna_id = comuna.id
            diccionario['comuna'][normalizar_texto(comprador['ComunaUnidad'])] = comuna_id
        else:
            comuna_id = diccionario['comuna'][normalizar_texto(comprador['ComunaUnidad'])]

        if not entidad_existe('unidad', comprador['RutUnidad'], diccionario):
            unidad = UnidadOrganismo(
                rut_unidad = comprador['RutUnidad'],
                codigo_unidad = comprador['CodigoUnidad'],
                nombre = normalizar_texto(comprador['NombreUnidad']),
                organismo_id = organismo_id,
                direccion = normalizar_texto(comprador['DireccionUnidad']),
                comuna_id = comuna_id,
            )

            unidad.save()

            unidad_id = unidad.id
            diccionario['unidad'][comprador['RutUnidad']] = unidad_id

        else:
            unidad_id = diccionario['unidad'][comprador['RutUnidad']]
        
        if not entidad_existe('persona', comprador['RutUsuario'], diccionario):
            persona = Persona(
                rut = comprador['RutUsuario'],
                nombre = normalizar_texto(comprador['NombreUsuario']),
                contacto = '',
                codigo_origen = comprador['CodigoUsuario'],
            )

            persona.save()
            persona_id = persona.id
            diccionario['persona'][comprador['RutUsuario']] = persona_id
        else:
            persona_id = diccionario['persona'][comprador['RutUsuario']]

        if not entidad_existe('cargo', normalizar_texto(comprador['CargoUsuario']), diccionario):
            cargo = Cargo(
                nombre = normalizar_texto(comprador['CargoUsuario']),
            )

            cargo.save()
            cargo_id = cargo.id
            diccionario['cargo'][normalizar_texto(comprador['CargoUsuario'])] = cargo_id
        else:
            cargo_id = diccionario['cargo'][normalizar_texto(comprador['CargoUsuario'])]
        
        persona_organismo = PersonaOrganismo(
            persona_id = persona_id,
            unidad_organismo_id = unidad_id,
            cargo_id = cargo_id,
            email = ''
        )

        persona_organismo.save()

    except Exception as e:
        print('###### Error en extraccion de Comprador')
        print(e)

    # Licitaciones
    try:
        if not entidad_existe('estado_licitacion', json_licitacion['CodigoEstado'], diccionario):
            estado_licitacion = EstadoLicitacion(
                codigo_origen = json_licitacion['CodigoEstado'],
                nombre = normalizar_texto(json_licitacion['Estado']),
            )

            estado_licitacion.save()
            estado_licitacion_id = estado_licitacion.id
            diccionario['estado_licitacion'][json_licitacion['CodigoEstado']] = estado_licitacion_id
        else:
            estado_licitacion_id = diccionario['estado_licitacion'][json_licitacion['CodigoEstado']]

        if not entidad_existe('tipo_licitacion', json_licitacion['CodigoTipo'], diccionario):
            tipo_licitacion = TipoLicitacion(
                codigo_origen = json_licitacion['CodigoTipo'],
                nombre = normalizar_texto(json_licitacion['Tipo']),
            )

            tipo_licitacion.save()
            tipo_licitacion_id = tipo_licitacion.id
            diccionario['tipo_licitacion'][json_licitacion['CodigoTipo']] = tipo_licitacion_id
        else:
            tipo_licitacion_id = diccionario['tipo_licitacion'][json_licitacion['CodigoTipo']]

        if not entidad_existe('licitacion', json_licitacion['CodigoExterno'], diccionario):
            licitacion = Licitacion(
                codigo = json_licitacion['CodigoExterno'],
                nombre = normalizar_texto(json_licitacion['Nombre']),
                
                estado_id = estado_licitacion_id,
                tipo_id = tipo_licitacion_id,
                
                descripcion = normalizar_texto(json_licitacion['Descripcion']),
                fecha_cierre = json_licitacion['FechaCierre'],
                informada = json_licitacion['Informada'],
                etapas = json_licitacion['Etapas'],
                moneda = json_licitacion['Moneda'],

                comprador = persona_organismo,

                fecha_creacion = json_licitacion['Fechas']['FechaCreacion'],
                fecha_inicio = json_licitacion['Fechas']['FechaInicio'],
                fecha_final = json_licitacion['Fechas']['FechaFinal'],
                fecha_pub_respuestas = json_licitacion['Fechas']['FechaPubRespuestas'],
                fecha_acto_apertura_tecnica = json_licitacion['Fechas']['FechaActoAperturaTecnica'],
                fecha_acto_apertura_economica = json_licitacion['Fechas']['FechaActoAperturaEconomica'],
                fecha_publicacion = json_licitacion['Fechas']['FechaPublicacion'],
                fecha_adjudicacion = json_licitacion['Fechas']['FechaAdjudicacion'],
                fecha_estimada_adjudicacion = json_licitacion['Fechas']['FechaEstimadaAdjudicacion'],
                fecha_soporte_fisico = json_licitacion['Fechas']['FechaSoporteFisico'],
                fecha_tiempo_evaluacion = json_licitacion['Fechas']['FechaTiempoEvaluacion'],
                fecha_estimada_firma = json_licitacion['Fechas']['FechaEstimadaFirma'],
                fechas_usuario = json_licitacion['Fechas']['FechasUsuario'],
                fecha_visita_terreno = json_licitacion['Fechas']['FechaVisitaTerreno'],
                fecha_entrega_antecedentes = json_licitacion['Fechas']['FechaEntregaAntecedentes'],
                url_acta_adjudicacion = json_licitacion['Adjudicacion']['UrlActa'],
            )

            # "TipoConvocatoria": "1",

            # "EstadoEtapas": "1",
            # "TomaRazon": "0",
            # "EstadoPublicidadOfertas": 1,
            # "JustificacionPublicidad": "Todas las ofertas técnicas serán visibles al público en general, través del portal www.mercadopublico.cl, desde el momento de la apertura electrónica.",
            # "Contrato": "0",
            # "Obras": "0",
            
            licitacion.save()
            licitacion_id = licitacion.id
            diccionario['licitacion'][json_licitacion['CodigoExterno']] = licitacion_id

    except Exception as e:
        print('###### Error en extraccion de Licitacion')
        print(e)
    
    # Items
    try:
        for item in json_licitacion['Items']['Listado']:
            if not entidad_existe('categoria_item', item['CodigoCategoria'], diccionario):
                categoria_item = CategoriaItem(
                    codigo_origen = item['CodigoCategoria'],
                    nombre = normalizar_texto(item['Categoria']),
                )

                categoria_item.save()
                categoria_item_id = categoria_item.id
                diccionario['categoria_item'][item['CodigoCategoria']] = categoria_item_id
            else:
                categoria_item_id = diccionario['categoria_item'][item['CodigoCategoria']]
            
            if not entidad_existe('item', item['CodigoProducto'], diccionario):
                item_model = Item(
                    codigo_producto = item['CodigoProducto'],
                    nombre = normalizar_texto(item['NombreProducto']),
                    categoria_id = categoria_item_id,
                )

                item_model.save()
                item_model_id = item_model.id
                diccionario['item'][item['CodigoProducto']] = item_model_id
            else:
                item_model_id = diccionario['item'][item['CodigoProducto']]
            
            if not entidad_existe('organismo_rut', item['Adjudicacion']['RutProveedor'], diccionario):
                proveedor = Organismo(
                    codigo_origen = '',
                    rut_organismo = item['Adjudicacion']['RutProveedor'],
                    nombre = normalizar_texto(item['Adjudicacion']['NombreProveedor']),
                    cantidad_reclamos = 0,
                )

                proveedor.save()
                proveedor_id = proveedor.id
                diccionario['organismo_rut'][item['Adjudicacion']['RutProveedor']] = proveedor_id
            else:
                proveedor_id = diccionario['organismo_rut'][item['Adjudicacion']['RutProveedor']]

            adjudicacion_item = AdjudicacionItem(
                organismo_proveedor_id = proveedor_id,
                cantidad = item['Adjudicacion']['Cantidad'],
                monto_unitario = item['Adjudicacion']['MontoUnitario'],
            )

            adjudicacion_item.save()
            
            item_licitacion = ItemLicitacion(
                item_id = item_model_id,
                correlativo = item['Correlativo'],
                unidad_medida = item['UnidadMedida'],
                cantidad = item['Cantidad'],
                adjudicacion = adjudicacion_item,
                descripcion = normalizar_texto(item['Descripcion']),
                licitacion_id = licitacion_id,
            )

            item_licitacion.save()

    except Exception as e:
        print('###### Error en extraccion de Items')
        print(e)

def entidad_existe(modelo, codigo, diccionario=None):
    if diccionario is None:
        diccionario = generar_diccionario()
    return codigo in diccionario[modelo].keys()

def generar_diccionario():
    diccionario = {}

    config = {
        'comuna': ('nombre', Comuna),
        'region': ('nombre', Region),
        'persona': ('rut', Persona),
        'cargo': ('nombre', Cargo),
        'unidad': ('rut_unidad', UnidadOrganismo),
        'estado_licitacion': ('codigo_origen', EstadoLicitacion),
        'tipo_licitacion': ('codigo_origen', TipoLicitacion),
        'organismo_codigo': ('codigo_origen', Organismo),
        'organismo_rut': ('rut_organismo', Organismo),
        'item': ('codigo_producto', Item),
        'categoria_item': ('codigo_origen', CategoriaItem),
        'licitacion': ('codigo', Licitacion),
    }

    for llave_config, tupla_config in config.items():
        diccionario[llave_config] = {
            instancia[tupla_config[0]]: instancia['id'] for instancia in list(
                tupla_config[1].objects.all().values('id', tupla_config[0])
            )
        }

    return diccionario

def normalizar_texto(texto):
    return unidecode.unidecode(texto.upper().strip())

def licitaciones_por_fecha(request):
    api = api_mercado_publico.ApiMercadoPublico()

    d = datetime.today().strftime("%Y-%m-%d")

    licitaciones_hoy = Licitacion.objects.filter(
        fecha_publicacion__gte = d
    )

    codigos = list(
        licitaciones_hoy.values_list('codigo', flat=True)
    )

    licitaciones_hoy_api = api.get_licitaciones_hoy()

    codigos_nuevos = [ l['CodigoExterno'] for l in licitaciones_hoy_api['Listado'] ]
    
    codigos_buscar_en_api = np.setdiff1d(codigos_nuevos, codigos)

    insertar_licitaciones_por_listado_codigos(codigos_buscar_en_api)

    licitaciones_hoy = Licitacion.objects.filter(
        fecha_publicacion__gte = d
    )

    return JsonResponse(
        {
            'licitaciones': list(licitaciones_hoy.values())
        }
    )

def insertar_licitaciones_por_listado_codigos(codigos):
    api = api_mercado_publico.ApiMercadoPublico()

    columnas = ['codigo_error']
    dd = pd.DataFrame(columns=columnas)
    i = 0
    total_licitaciones = len(codigos)
    for codigo in codigos:
        try:
            time.sleep(2)
            licitacion_completa = api.get_licitacion_por_codigo(codigo)['Listado'][0]

            extractor(licitacion_completa)
        except Exception as e:
            print(e)
            dd = dd.append({ 'codigo_error': codigo }, ignore_index=True)
        print("###################################")
        i += 1
        print("procesada: ", i)
        print("total: {0}/{1}".format(i, total_licitaciones), " -> ", (i*1.0)/total_licitaciones)
        print("###################################")
    dd.to_excel('/home/ronofri/Escritorio/licitaciones_con_error.xlsx')

#Agregar una forma de 
def update_licitacion():
    pass

def get_sample_licitaciones(request):
    n = 600
    licitaciones = Licitacion.objects.all().select_related('estado').select_related('tipo')
    licitaciones = licitaciones.select_related('comprador').select_related('comprador__persona')
    licitaciones = licitaciones.select_related('comprador__unidad_organismo').select_related('comprador__unidad_organismo__organismo')
    licitaciones = licitaciones.select_related('comprador__unidad_organismo__comuna').select_related('comprador__unidad_organismo__comuna__region')
    licitaciones = licitaciones.select_related('comprador__cargo')[:n]

    codigos = set([ lic.codigo for lic in licitaciones ])

    items_licitacion = ItemLicitacion.objects.filter(licitacion__codigo__in=codigos).select_related('adjudicacion')
    items_licitacion = items_licitacion.select_related('adjudicacion__organismo_proveedor')
    items_licitacion = items_licitacion.select_related('licitacion')
    items_licitacion = items_licitacion.select_related('item')

    items_dict = {}

    for ii in items_licitacion:
        codigo_licitacion = ii.licitacion.codigo
        if codigo_licitacion not in items_dict.keys():
            items_dict[codigo_licitacion] = []
        items_dict[codigo_licitacion].append(
            {
                'item': ii.item.nombre,
                'rut': ii.adjudicacion.organismo_proveedor.rut_organismo,
                'proveedor': ii.adjudicacion.organismo_proveedor.nombre,
                'cantidad': ii.adjudicacion.cantidad,
                'monto_unitario': ii.adjudicacion.monto_unitario,
            }
        )
    
    resultados = []

    for lic in licitaciones:
        resultados.append(
            {
                'licitacion__codigo': lic.codigo,
                'licitacion__nombre': lic.nombre,
                'licitacion__estado': lic.estado.nombre,
                'licitacion__descripcion': lic.descripcion,
                'licitacion__fecha_cierre': lic.fecha_cierre,
                'comprador__codigo': lic.comprador.unidad_organismo.organismo.codigo_origen,
                'comprador__rut': lic.comprador.unidad_organismo.organismo.rut_organismo,
                'comprador__nombre': lic.comprador.unidad_organismo.organismo.nombre,
                'comprador__persona__rut': lic.comprador.persona.rut,
                'comprador__persona__nombre': lic.comprador.persona.nombre,
                'comprador__persona__cargo': lic.comprador.cargo.nombre,
                'licitacion__tipo': lic.tipo.nombre,
                'licitacion__moneda': lic.moneda,
                'licitacion__etapas': lic.etapas,
                'licitacion__informada': lic.informada,
                'licitacion__fecha_creacion': lic.fecha_creacion.strftime('%d-%m-%Y') if lic.fecha_creacion is not None else '',
                'licitacion__fecha_inicio': lic.fecha_inicio.strftime('%d-%m-%Y') if lic.fecha_inicio is not None else '',
                'licitacion__fecha_final': lic.fecha_final.strftime('%d-%m-%Y') if lic.fecha_final is not None else '',
                'licitacion__fecha_pub_respuestas': lic.fecha_pub_respuestas.strftime('%d-%m-%Y') if lic.fecha_pub_respuestas is not None else '',
                'licitacion__fecha_acto_apertura_tecnica': lic.fecha_acto_apertura_tecnica.strftime('%d-%m-%Y') if lic.fecha_acto_apertura_tecnica is not None else '',
                'licitacion__fecha_acto_apertura_economica': lic.fecha_acto_apertura_economica.strftime('%d-%m-%Y') if lic.fecha_acto_apertura_economica is not None else '',
                'licitacion__fecha_publicacion': lic.fecha_publicacion.strftime('%d-%m-%Y') if lic.fecha_publicacion is not None else '',
                'licitacion__fecha_adjudicacion': lic.fecha_adjudicacion.strftime('%d-%m-%Y') if lic.fecha_adjudicacion is not None else '',
                'licitacion__fecha_estimada_adjudicacion': lic.fecha_estimada_adjudicacion.strftime('%d-%m-%Y') if lic.fecha_estimada_adjudicacion is not None else '',
                'licitacion__fecha_soporte_fisico': lic.fecha_soporte_fisico.strftime('%d-%m-%Y') if lic.fecha_soporte_fisico is not None else '',
                'licitacion__fecha_tiempo_evaluacion': lic.fecha_tiempo_evaluacion.strftime('%d-%m-%Y') if lic.fecha_tiempo_evaluacion is not None else '',
                'licitacion__fecha_estimada_firma': lic.fecha_estimada_firma.strftime('%d-%m-%Y') if lic.fecha_estimada_firma is not None else '',
                'licitacion__fechas_usuario': lic.fechas_usuario.strftime('%d-%m-%Y') if lic.fechas_usuario is not None else '',
                'licitacion__fecha_visita_terreno': lic.fecha_visita_terreno.strftime('%d-%m-%Y') if lic.fecha_visita_terreno is not None else '',
                'licitacion__fecha_entrega_antecedentes': lic.fecha_entrega_antecedentes.strftime('%d-%m-%Y') if lic.fecha_entrega_antecedentes is not None else '',
                'licitacion__url_acta_adjudicacion': lic.url_acta_adjudicacion,
                'licitacion__items': items_dict[lic.codigo] if lic.codigo in items_dict.keys() else []
            }
        )

    df = pd.DataFrame(resultados)

    df.to_excel('/home/ronofri/Escritorio/licitaciones_sample.xlsx')
    
    return JsonResponse( { 'licitaciones': resultados } )
