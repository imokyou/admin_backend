# coding=utf8
import json
import traceback
from Cookie import SimpleCookie
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.views import logout as auth_logout
from django.http.response import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from lib import utils
from config import errors

class CustomCookie(SimpleCookie):
    
    def value_decode(self, val):
        return val, val

    def value_encode(self, val):
        strval = str(val)
        return strval, val


def test(request):
    return utils.NormalResp()


@csrf_exempt
@require_http_methods(['POST'])
def login(request):
    try:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if not username or not password:
            return utils.ErrResp(errors.ArgMis)
        
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            return utils.ErrResp(errors.UserNotExists)
    
        response = HttpResponseRedirect(settings.SITE_URL)
        resp_cookies = CustomCookie()
        expires = 3600
        resp_cookies['email'] = user.email
        resp_cookies['email']['expires'] = expires
        resp_cookies['email']['path'] = '/'
        
        resp_cookies['Account'] = username
        resp_cookies['Account']['expires'] = expires
        resp_cookies['Account']['path'] = '/'
        response.cookies = resp_cookies
        auth_login(request, user)
        return response
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)
    return utils.NormalResp()


@csrf_exempt
def logout(request):
    response = auth_logout(request, next_page=settings.REDIRECT_LOGIN_URI)
    response.delete_cookie('email')
    response.delete_cookie('Account')
    return response
