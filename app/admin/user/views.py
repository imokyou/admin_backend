# coding=utf8
import json
import traceback
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User as Auth_User
from lib import utils
from config import errors


ROLE2NAME = {
    1: '超管',
    0: '一般管'
}

STATUS2NAME = {
    1: '正常',
    0: '封停'
}


@csrf_exempt
def test(request):
    return utils.NormalResp()

@csrf_exempt
def get_list(request):
    try:
        p = request.GET.get('p', 1)
        n = request.GET.get('n', 30)
        username = request.GET.get('account')
        is_superuser = int(request.GET.get('role', -1))
        is_active = int(request.GET.get('status', -1))

        q = Auth_User.objects
        if username:
            q = q.filter(username__icontains=username)
        if is_superuser != -1:
            q = q.filter(is_superuser=is_superuser)
        if is_active != -1:
            q = q.filter(is_active=is_active)

        tot = q.count()
        q = q.order_by('-id')
        users = q.all()[(p-1)*n:p*n]

        data = []
        for u in users:
            info = {
                'id': u.id,
                'account': u.username,
                'email': u.email,
                'created_at': u.date_joined.strftime('%Y-%m-%d %H:%m:%S'),
                'role': int(u.is_superuser),
                'role_name': ROLE2NAME[u.is_superuser],
                'status': int(u.is_active),
                'status_name': STATUS2NAME[u.is_active]
            }
            data.append(info)
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)
    d = {'tot': tot, 'p': p, 'n': n, 'data': data}
    return utils.NormalResp(d)


@csrf_exempt
def info(request):
    try:
        aid = int(request.GET.get('id', 0))
        if not aid:
            return utils.ErrResp(errors.ArgMis)
        
        try:
            u = Auth_User.objects.get(id=aid)
        except:
            return utils.ErrResp(errors.UserNotExists)
        info = {
            'id': u.id,
            'account': u.username,
            'email': u.email,
            'created_at': u.date_joined.strftime('%Y-%m-%d H:M:S'),
            'role': u.is_superuser,
            'role_name': ROLE2NAME[u.is_superuser],
            'status': u.is_active,
            'status_name': STATUS2NAME[u.is_active],
            'password': ''
        }
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)
    return utils.NormalResp(info)


@csrf_exempt
@require_http_methods(['POST'])
def new(request):
    try:
        username = request.POST.get('account', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')
        is_superuser = request.POST.get('role', 0)

        username_exists = Auth_User.objects.filter(username=username).count()
        if username_exists:
            return utils.ErrResp(errors.UserExists)
        email_exists = Auth_User.objects.filter(email=email).count()
        if email_exists:
            return utils.ErrResp(errors.EmailExists)

        if not username or not password or not email:
            return utils.ErrResp(errors.ArgMis)
        u = Auth_User.objects.create_user(username, email, password)
        u.is_superuser = is_superuser
        u.save()
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)
    return utils.NormalResp({'id': u.id})


@csrf_exempt
@require_http_methods(['POST'])
def update(request):
    try:
        aid = int(request.POST.get('id', 0))
        email = request.POST.get('email', '')
        is_superuser = int(request.POST.get('role', -1))
        is_active = int(request.POST.get('status', -1))
        password = request.POST.get('password', '')

        if not aid:
            return utils.ErrResp(errors.ArgMis)
        try:
            u = Auth_User.objects.get(id=aid)
        except:
            return utils.ErrResp(errors.UserNotExists)
        
        if email:
            email_exists = Auth_User.objects.filter(email=email).count()
            if email_exists:
                return utils.ErrResp(errors.EmailExists)
            u.email = email
        if is_superuser != -1:
            u.is_superuser = is_superuser
        if is_active != -1:
            u.is_active = is_active
        if password:
            u.set_password(password)
        u.save()
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)
    return utils.NormalResp({'id': aid})