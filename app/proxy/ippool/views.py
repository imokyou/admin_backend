# coding=utf8
import traceback
from lib import utils
from config import errors
from db import RedisClient


def test(request):
    return utils.NormalResp()


def get_list(request):
    try:
        p = request.GET.get('p', 1)
        n = request.GET.get('n', 100)

        redisdb = RedisClient()
        proxies = redisdb.get_allproxy()
        tot = redisdb.proxy_len
        data = []
        for proxy in proxies:
            info = {
                'proxy': proxy,
                'proto': proxy.split('://')[0].upper(),
                'ip': proxy.split('://')[1].split(':')[0],
                'port': proxy.split('://')[1].split(':')[1]
            }
            data.append(info)
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)
    d = {'tot': tot, 'p': p, 'n': n, 'data': data}
    return utils.NormalResp(d)