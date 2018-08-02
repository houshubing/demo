import requests
from django.conf import settings


def get_wb_access_token(code):
    args = settings.WB_ACCESS_TOKEN_ARGS.copy()
    args['code'] = code
    response = requests.post(settings.WB_ACCESS_TOKEN_API,data=args)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return {'error': 'weibo server error'}


def get_wb_user_show(access_token, uid):
    args = settings.WB_ACCESS_TOKEN_ARGS.copy()
    args['access_token'] = access_token
    args['uid'] = uid
    response = requests.post(settings.WB_ACCESS_TOKEN_API,params=args)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return {'error': 'weibo server error'}
