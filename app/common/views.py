# coding=utf8
import json
from lib import utils


def test(request):
    data = {}
    for key in request.META:
        if key not in data:
            data[key] = request.META[key]
    return utils.NormalResp(str(data))
