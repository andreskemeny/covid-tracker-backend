from django.shortcuts import render

# REST framework imports
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.views import Response

# Processing the data
import json
import requests

# Caching policy imports
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class StatViewSet(viewsets.ViewSet):
    # usamos un action de un viewset para poder tener acceso al cache, definimos el tipo de accion y el url del endpoint
    @method_decorator(cache_page(43200))
    @action(methods=['GET'], detail=False, url_path='chile')
    def chile(self, request):
        try:
            # llama a la api
            res = requests.get(
                "https://chile-coronapi.herokuapp.com/api/v3/historical/nation")

            # nos devuelve json, lo tenemos que procesar y convertir en un diccionario que python puede leer.
            processed_res = json.loads(res.text)

            # definimos las variables que nuestra api va a devolvernos
            casos, fechas, muertes = [], [], []
            for x in processed_res:
                fechas.append(x)
                casos.append(processed_res[x]['confirmed'])
                muertes.append(processed_res[x]['deaths'])

            # acceder al ultimo elemento de la respuesta de la api y extraer el numero que corresponde a "confirmed_per_million"
            confirmed_per_million = processed_res[fechas[-1]
                                                  ]['confirmed_per_million']
            # acceder al ultimo elemento de la respuesta de la api y extraer el numero de casos hasta ese punto
            total_cases = casos[-1]
            # calcular el fatality rate que corresponde al numero de muertes dividido en el numero de casos totales y eso multiplicado por 100
            fatality_rate = str((muertes[-1]/total_cases)*100)[:3]

            # la api nos devuelve las variables que asignamos mas arriba con status 200 (exito)
            return Response({
                "casos": casos[-61:],
                "fechas": fechas[-61:],
                "muertes": muertes[-61:],
                "confirmed_per_million": confirmed_per_million,
                "total_cases": total_cases,
                "fatality_rate": fatality_rate
            }, status=status.HTTP_200_OK)

        # en caso de toparse una excepcion nos devuelve el error y status 400 (bad request)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(cache_page(43200))
    @action(methods=['GET'], detail=False, url_path='chile_communes')
    def chile_communes(self, request):
        try:
            communes = ['Alhue', 'Buin', 'Calera de Tango', 'Cerrillos',
                        'Cerro navia', 'Colina', 'Conchalí', 'Curacaví', 'El Bosque', 'El Monte',
                        'Estación Central', 'Huechuraba', 'Independencia', 'Isla de Maipo', 'La Cisterna',
                        'La Florida', 'La Granja', 'La Pintana', 'La Reina', 'Lampa', 'Las Condes', 'Lo Barnechea',
                        'Lo Espejo', 'Lo Prado', 'Macul', 'Maipú', 'Melipilla', 'María Pinto', 'Ñuñoa', 'Padre Hurtado',
                        'Pedro Aguirre Cerda', 'Paine', 'Peñaflor', 'Peñalolen', 'Pirque', 'Providencia', 'Pudahuel',
                        'Puente Alto', 'Quilicura', 'Quinta Normal', 'Recoleta', 'Renca', 'San Bernardo',
                        'San Joaquín', 'San José de Maipo', 'San Miguel', 'San Pedro', 'San Ramón', 'Santiago Centro',
                        'Talagante', 'Til Til', 'Vitacura']

            commune_states = ['No', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si',
                              'Si', 'No', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si',
                              'Si', 'Si', 'Si', 'No', 'Si', 'Si', 'Si', 'No', 'Si', 'Si', 'No', 'Si',
                              'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'No', 'Si',
                              'Si', 'Si', 'Si', 'Si']

            return Response({"communes": communes, "states": commune_states}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(cache_page(43200))
    @action(methods=['GET'], detail=False, url_path='world')
    def world(self, request):
        try:
            res = requests.get(
                "https://corona.lmao.ninja/v2/countries?yesterday&sort=cases")

            processed_res = json.loads(res.text)

            recuperation_percentage_cl = 0
            total_cases = 0
            map_data = {}
            for country_data in processed_res:
                map_data[country_data["countryInfo"]
                         ["iso2"]] = country_data["cases"]
                total_cases += country_data["cases"]
                if country_data["country"] == "Chile":
                    recuperation_percentage_cl = str(
                        (country_data["recovered"]/country_data["cases"])*100)[:4]

            top_6 = []
            for i in range(6):
                percentOfTotal = str(
                    (processed_res[i]["cases"]/total_cases)*100)[:4]
                top_6.append({"country": processed_res[i]["country"], "cases": processed_res[i]
                              ["cases"], "flag": processed_res[i]["countryInfo"]["flag"], "percentOfTotal": percentOfTotal})

            return Response({"map_data": map_data, "top_6": top_6, "recuperation_percentage_cl": recuperation_percentage_cl}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


"""
@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})
"""
