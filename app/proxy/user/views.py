# coding=utf8
import traceback
from lib import utils
from dbmodel.proxy.models import User
from config import errors


def test(request):
    return utils.NormalResp()


def get_list(request):
    try:
        p = request.GET.get('p', 1)
        n = request.GET.get('n', 30)
        email = request.GET.get('email')

        q = User.objects
        if email:
            q = q.filter(email__icontains=email)

        tot = q.count()
        q = q.order_by('-id')
        users = q.all()[(p-1)*n:p*n]

        data = []
        for u in users:
            info = {
                'id': u.id,
                'email': u.email,
                'contact': u.contact,
                'created_at': u.created_at.strftime('%Y-%m-%d %H:%m:%S'),
                'updated_at': ''
            }
            try:
                info['updated_at'] = u.updated_at.strftime('%Y-%m-%d %H:%m:%S'),
            except:
                pass
            data.append(info)
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)
    d = {'tot': tot, 'p': p, 'n': n, 'data': data}
    return utils.NormalResp(d)