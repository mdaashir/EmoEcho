from django.shortcuts import render

import json
import requests

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse

@api_view(['POST'])
def getAuthorizationCode(request):
    if request.method == 'POST':
        client_id = request.data.get('client_id')
        redirect_uri = request.data.get('redirect_uri')
        scope = request.data.get('scope')
        response_type = request.data.get('response_type')
        url = f'https://api.instagram.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type={response_type}'
        return JsonResponse({'response': url})   
    
@api_view(['POST'])
def getAccessToken(request):
    if request.method == 'POST':
        url = "https://api.instagram.com/oauth/access_token"
        data = {
            'client_id': request.data.get('client_id'),
            'client_secret':  request.data.get('client_secret'),
            'grant_type': 'authorization_code',
            'redirect_uri':  request.data.get('redirect_uri'),
            'code':  request.data.get('code'),
        }
        try:
            response = requests.post(url, data=data)
            response_data = json.loads(response.text)
            if response.status_code == 200:
                response = getLongLivedAcessToken(response_data["access_token"], request.data.get('client_secret'),response_data["user_id"])
                return response
            else:
                return JsonResponse({'error': f'Failed to get Access Token {response.status_code}'}, status=500)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Error decoding JSON data: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

def getLongLivedAcessToken(access_token, client_secret, user_id):
    url = f"https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret={client_secret}&access_token={access_token}"
    try:
        response = requests.get(url)
        response_data = json.loads(response.text)
        if response.status_code == 200:
            return JsonResponse({'access_token': response_data["access_token"],'user_id': user_id, 'expires_in': response_data["expires_in"]})
        else:
            return JsonResponse({'error': f'Failed to get Long Lived Access Token {response.status_code}'}, status=500)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': f'Error decoding JSON data: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
        
@api_view(['POST'])
def getUserDetails(request):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        access_token = request.data.get('access_token')
        url = f"https://graph.instagram.com/{user_id}?fields=id,username&access_token={access_token}"
        try:
            response = requests.get(url)
            response_data = json.loads(response.text)
            if response.status_code == 200:
                return JsonResponse({'response': response_data})
            else:
                return JsonResponse({'error': f'Failed to get User Details {response.status_code}'}, status=500)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Error decoding JSON data: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

@api_view(['POST'])
def getUserPosts(request):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        access_token = request.data.get('access_token')
        url = f"https://graph.instagram.com/{user_id}/media?fields=id,username,caption,media_type,media_url&access_token={access_token}"
        try:
            response = requests.get(url)
            response_data = json.loads(response.text)
            if response.status_code == 200:
                return JsonResponse({'response': response_data})
            else:
                return JsonResponse({'error': f'Failed to get User Posts {response.status_code}'}, status=500)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Error decoding JSON data: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)