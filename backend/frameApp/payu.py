import http.client
import json
import uuid
import requests
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Frame
from userApp.models import MyUser

PAYU_POS_ID = 478178
PAYU_SECOND_KEY = 'cef91e0035a7ee39b7702b5df63c0bdf'
PAYU_CLIENT_ID = 478178
PAYU_CLIENT_SECRET = 'bf42a37f3bfb9e4317f58d5840a04d02'
PAYU_AUTHORIZATION_URL = 'https://secure.snd.payu.com/pl/standard/user/oauth/authorize'
PAYU_ORDER_URL = 'https://secure.snd.payu.com/api/v2_1/orders'
PAYU_OAUTH_URL = 'https://secure.snd.payu.com/pl/standard/user/oauth/authorize'


def get_payu_token(request):
    data = {
        'grant_type': 'client_credentials',
        'client_id': PAYU_CLIENT_ID,
        'client_secret': PAYU_CLIENT_SECRET,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(PAYU_OAUTH_URL, data=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to get token", "status": response.status_code, "details": response.text}


def create_order(request, frame_id):
    try:
        frame = get_object_or_404(Frame, pk=frame_id)
        user = request.user
        token_data = get_payu_token(request)
        access_token = token_data.get('access_token')

        order = json.dumps({
            "notifyUrl": "https://13da-88-156-14-190.ngrok-free.app/frameApp/notify",
            "customerIp": "123.123.123.123",
            "merchantPosId": PAYU_POS_ID,
            "description": "Zakup ramki",
            "currencyCode": "PLN",
            "totalAmount": str(int(frame.price * 100)),
            "extOrderId": str(uuid.uuid4()),
            "buyer": {
                "email": user.email,
                "firstName": user.username,
            },
            "products": [
                {
                    "name": frame.frame_name,
                    "unitPrice": str(int(frame.price * 100)),
                    "quantity": "1"
                }
            ]
        })

        request.session['purchased_frame_id'] = frame_id

        conn = http.client.HTTPSConnection("secure.snd.payu.com")
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        conn.request("POST", "/api/v2_1/orders", body=order, headers=headers)
        response = conn.getresponse()
        response_data = response.read().decode('utf-8')

        data_dict = json.loads(response_data)

        order_id = data_dict['orderId']
        request.session['order_id'] = order_id

        conn.close()

        if response.status in (200, 201, 302):
            response_json = json.loads(response_data)

            redirect_uri = response_json.get('redirectUri')

            if redirect_uri:
                return HttpResponseRedirect(redirect_uri)
            else:
                return JsonResponse({"error": "Redirect URI not found"}, status=404)
        else:
            return JsonResponse({"error": response_data}, status=response.status)
    except Exception as e:
        return JsonResponse({'error': 'Internal server error', 'details': str(e)}, status=500)


# @csrf_exempt
def payment_success(request):
    try:
        token_data = get_payu_token(request)
        access_token = token_data.get('access_token')

        frame_id = request.session.get('purchased_frame_id')
        frame = Frame.objects.get(id=frame_id)
        user = request.user

        conn = http.client.HTTPSConnection("secure.snd.payu.com")
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        conn.request("GET", f"/api/v2_1/orders/{request.session['order_id']}", headers=headers)
        response = conn.getresponse()
        response_data = response.read().decode('utf-8')
        response_json = json.loads(response_data)
        conn.close()

        if response_json['status']['statusCode'] == 'SUCCESS':
            user.avatar = frame.frame_url
            user.save()
            del request.session['purchased_frame_id']

            return HttpResponse("Płatność została zakończona pomyślnie i avatar został zaktualizowany.")

        else:
            return HttpResponse("Płatność nieudana lub w trakcie realizacji.", status=400)

    except Frame.DoesNotExist:
        return HttpResponse("Ramka nie istnieje.", status=404)
    except Exception as e:
        return HttpResponse(f"Wewnętrzny błąd serwera: {str(e)}", status=500)
