from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
import jwt
from Utils.utils import jwt_decode_handler
from user.models import User


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        '''返回一个元组，包含request.user和request.auth'''
        #获取jwt的值
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None
        try:   #如果存在，就对jwt进行解码
            payload = jwt_decode_handler(jwt_value)['data']
        except jwt.ExpiredSignature:  #如果token过期，则返回错误
            msg = 'Token过期'
            raise exceptions.AuthenticationFailed({'message': msg, 'errorCode': 1, 'data': {}})
        except jwt.DecodeError:
            msg = 'Token不合法'
            raise exceptions.AuthenticationFailed({'message': msg, 'errorCode': 1, 'data': {}})
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()
        user = self.authenticate_credentials(payload)   #解码成功后，返回用户
        return user, jwt_value


    def get_jwt_value(self, request):         #包含在请求头发过来的
        # auth = request.query_params.get('token')  #从请求的参数里接受token
        # if not auth:   #如果没有token 返回
        #     return ({'msg':'没有获取到token'})
        # return auth
        authorization = request.META.get('HTTP_AUTHORIZATION', '')
        auth = authorization.split()
        if not auth:
            raise exceptions.AuthenticationFailed({'msg': '未获取到请求头', 'errorCode': '2', 'data': {}})
        if auth[0].lower() != 'jwt':
            raise exceptions.AuthenticationFailed({'msg': '非法的请求头1', 'errorCode': '2', 'data': {}})
        if len(auth) == 1:
            raise exceptions.AuthenticationFailed({'msg': '非法的请求头2', 'errorCode': '2', 'data': {}})
        if len(auth) > 2:
            raise exceptions.AuthenticationFailed({'msg': '非法的请求头3', 'errorCode': '2', 'data': {}})
        token = auth[1]
        # result = jwt_decode_handler(token)  #此处用id好一些
        # if not result['status']:
        #     raise exceptions.AuthenticationFailed(result)
        return token



    #获取包含在token涨的用户id
    def authenticate_credentials(self, payload):  #此处用id好一些
        id1 = payload.get('id')
        if not id1:
            raise exceptions.AuthenticationFailed({'message': '没有该用户', 'errorCode': 1, 'data': {}})
        try:
            user = User.objects.filter(id=id1).first()
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed({'message':'没有该用户', 'errormsg': 1, 'data': {}})
        return user
