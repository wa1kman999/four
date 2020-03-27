import datetime
import jwt
from django.conf import settings

JWT_SALT = settings.SECRET_KEY

#生成一个token
def create_token(payload, timeout=200):   #过期时间可能还需要配置
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    result = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers).decode('utf-8')
    return result



def jwt_decode_handler(token):  #获取token
    result = {'status': False, 'data': None, 'error': None}
    try:
        verified_payload = jwt.decode(token, JWT_SALT, True)
        result['status'] = True
        result['data'] = verified_payload
    except jwt.ExpiredSignatureError:
        result['error'] = 'token已失效'
    except jwt.DecodeError:
        result['error'] = 'token认证失败'
    except jwt.InvalidTokenError:
        result['error'] = '非法的token'
    return result


def is_valid_mobile_phone(phone):
    '''
    判断是否为手机号
    '''
    import re
    return re.match('^1[34578]\d{9}$', phone)


def is_safe_password(password):
    '''
    检查密码强度
    密码要求包含大小写字母和数字,密码长度至少8位
    '''
    import re
    return re.match('(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$', password)
