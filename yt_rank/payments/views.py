from django.shortcuts import render,redirect,HttpResponse
from coinbase_commerce.client import Client
from coinbase_commerce.error import SignatureVerificationError, WebhookInvalidPayload
from coinbase_commerce.webhook import Webhook

from config import settings

# Create your views here.
# def point_page_view(request):
#     return render(request, 'payments/point_page.html')
from .models import PointValue,TokenPoint
from .forms import CreatePaymentForm
from common.models import User
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str as force_text

from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib import auth
import logging
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.models import Token
from django.contrib.sites.shortcuts import get_current_site
from common.telegram import send_to_telegram
def point_page_view(request):
    point_value = PointValue.objects.all().first()
    if point_value is None:
        return HttpResponse('포인트 가격이 설정되지 않았습니다. 관리자에게 문의하십시오.')
    return render(request, 'payments/point_page.html', {'point_value':point_value})

def create_charge(request, username):
    form = CreatePaymentForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            print(username)

            user = User.objects.get(username=username)
            # m_user = M_User.objects.get(username=username)
            uid= urlsafe_base64_encode(force_bytes(force_bytes(user.pk))).encode().decode()
            # token= account_activation_token.make_token(user)

            last_token = Token.objects.filter(user=user).first()
            if last_token is not None:
                last_token.delete()

            token = Token.objects.create(user=user)
            order_point = form.cleaned_data.get('order_point')

            TokenPoint.objects.create(key=token,point=int(order_point),status='ordering')
            # token_point.point = int(order_point)
            # token_point.save()
            point_value = PointValue.objects.all().first()
            point_price = point_value.point_price
            order_value = order_point*point_price
            client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
            current_site = get_current_site(request)
            domain_url = current_site.domain + '/'
            if not 'http://' in domain_url:
                domain_url = 'https://' + domain_url
            product = {
                'name': f'{order_point} 포인트',
                'description': '포인트를 충전합니다.', #domain_url + 'payments/success/' + f"{uid}/{token}/",
                'local_price': {
                    'amount': f"{order_value}",
                    'currency': 'KRW'
                },
                'pricing_type': 'fixed_price',
                'redirect_url': domain_url + 'payments/success/' + f"{uid}/{token}/",
                'cancel_url': domain_url + 'payments/cancel/' + f"{uid}/",
                'metadata':{
                    'username':username,
                    'uid64': uid,
                    'token_info': token.key,
                    'order_point': order_point,
                },
            }
            print(3)
            charge = client.charge.create(**product)
            print(4)
            return redirect(charge.hosted_url)
    return render(request, 'payments/point_page.html', {'form': form})

def success_view(request, uid64, token):
    uid = force_text(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)
    token = Token.objects.filter(user=user,key=token).first()
    if token is None:
        return HttpResponse('만료된 요청 또는 이미 반영된 요청입니다.')
    if user is not None:
        token_point = TokenPoint.objects.get(key=token)
        token.delete()
        order_point = token_point.point
        user.point = user.point + order_point
        msg = f"신규충전\n{user.username}\n{order_point}포인트"
        send_to_telegram(msg)
        user.save()
        return render(request, 'payments/success.html')
    else:
        return HttpResponse('비정상적인 접근입니다.')

def cancel_view(request, uid64):
    uid = force_text(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)
    token = Token.objects.filter(user=user).first()
    if token is None:
        return HttpResponse('만료된 요청 또는 이미 반영된 요청입니다.')
    if user is not None:
        msg = f"신규충전 취소\n{user.username}"
        send_to_telegram(msg)
        token.delete()
        return render(request, 'payments/cancel.html')
    else:
        return HttpResponse('비정상적인 접근입니다.')


@csrf_exempt
@require_http_methods(['POST'])
def coinbase_webhook(request):
    # logger = logging.getLogger(__name__)

    request_data = request.body.decode('utf-8')
    request_sig = request.headers.get('X-CC-Webhook-Signature', None)
    webhook_secret = settings.COINBASE_COMMERCE_WEBHOOK_SHARED_SECRET

    try:
        event = Webhook.construct_event(request_data, request_sig, webhook_secret)

        # List of all Coinbase webhook events:
        # https://commerce.coinbase.com/docs/api/#webhooks
        uid64 = event['data']['metadata']['uid64']  # new
        token = event['data']['metadata']['token_info']  # new
        uid = force_text(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
        token = Token.objects.filter(user=user, key=token).first()
        if token is None:
            return HttpResponse('만료된 요청입니다.')
        if event['type'] == 'charge:confirmed':
            # logger.info('Payment confirmed.')
            if user is not None:
                token_point = TokenPoint.objects.get(key=token)
                token.delete()
                order_point = token_point.point
                user.point = user.point + order_point
                user.save()
        elif event['type'] == 'charge:created':
            if user is not None:
                token_point = TokenPoint.objects.get(key=token)
                token_point.status = 'created'
                token_point.save()
        elif event['type'] == 'charge:delayed':
            if user is not None:
                token_point = TokenPoint.objects.get(key=token)
                token_point.status = 'delayed'
                token_point.save()
        elif event['type'] == 'charge:failed':
            if user is not None:
                token_point = TokenPoint.objects.get(key=token)
                token_point.status = 'failed'
                token_point.save()
        elif event['type'] == 'charge:pending':
            if user is not None:
                token_point = TokenPoint.objects.get(key=token)
                token_point.status = 'pending'
                token_point.save()
        elif event['type'] == 'charge:resolved':
            if user is not None:
                token_point = TokenPoint.objects.get(key=token)
                token_point.status = 'resolved'
                token_point.save()

    except (SignatureVerificationError, WebhookInvalidPayload) as e:
        return HttpResponse(e, status=400)

    # logger.info(f'Received event: id={event.id}, type={event.type}')
    return HttpResponse('ok', status=200)