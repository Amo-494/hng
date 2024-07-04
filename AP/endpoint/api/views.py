from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests

# Create your views here.
# api/views.py


@api_view(['GET'])
def hng_view(request):
    name = request.query_params.get('name')
    client_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')

    geo = requests.get(f'http://ip-api.com/json/{client_ip}').json()
    location = geo.get('city', 'Unknown location')

    weather_response = requests.get(f'http://api.weatherapi.com/v1/current.json?key=010de130219a43d59aa225838240307&q={location}')
    weather_data = weather_response.json()

    if 'error' in weather_data:
        error_message = weather_data['error']['message']
        return Response({'error': f"Error from Weather API: {error_message}"}, status=status.HTTP_400_BAD_REQUEST)
    
    temperature = weather_data.get('current', {}).get('temp_c', 'N/A')

    response_data = {
        'client_ip': client_ip,
        'location': location,
        'greeting': f'Hello, {name}!, the temperature is {temperature} degrees Celsius in {location}'
    }

    return Response(response_data)