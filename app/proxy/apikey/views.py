# coding=utf8
import traceback
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from lib import utils
from dbmodel.proxy.models import ApiKey
from config import errors


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
        owner = request.GET.get('owner')
        key = request.GET.get('key')
        status = int(request.GET.get('status', -1))

        q = ApiKey.objects
        if owner:
            q = q.filter(owner__icontains=owner)
        if key:
            q = q.filter(key=key)
        if status != -1:
            q = q.filter(status=status)

        tot = q.count()
        q = q.order_by('-id')
        users = q.all()[(p-1)*n:p*n]

        data = []
        for u in users:
            info = {
                'id': u.id,
                'owner': u.owner,
                'key': u.key,
                'created_at': u.created_at.strftime('%Y-%m-%d %H:%m:%S'),
                'status': int(u.status),
                'status_name': STATUS2NAME[u.status]
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
            u = ApiKey.objects.get(id=aid)
        except:
            return utils.ErrResp(errors.UserNotExists)
        info = {
            'id': u.id,
            'owner': u.owner,
            'key': u.key,
            'created_at': u.created_at.strftime('%Y-%m-%d %H:%m:%S'),
            'status': int(u.status),
            'status_name': STATUS2NAME[u.status]
        }
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)
    return utils.NormalResp(info)


@csrf_exempt
@require_http_methods(['POST'])
def new(request):
    try:
        owner = request.POST.get('owner', '')
        key = request.POST.get('key', '')

        if not owner or not key:
            return utils.ErrResp(errors.ArgMis)
        key_exists = ApiKey.objects.filter(key=key).count()
        if key_exists:
            return utils.ErrResp(errors.DataExists)
        
        u = ApiKey(
            owner=owner,
            key=key,
            status=1
        )
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
        status = int(request.POST.get('status', -1))

        if not aid:
            return utils.ErrResp(errors.ArgMis)
        try:
            u = ApiKey.objects.get(id=aid)
        except:
            return utils.ErrResp(errors.UserNotExists)
        
        if status != -1:
            u.status = status
        u.save()
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)
    return utils.NormalResp({'id': aid})