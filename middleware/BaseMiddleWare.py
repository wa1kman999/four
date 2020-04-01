# 权限 加密中间件
import re

from django.utils.deprecation import MiddlewareMixin

#
# class PermissionMiddleware(MiddlewareMixin):
#
#     def process_request(self, request):
#         white_paths = ['/adminlogin/']
#         if request.path not in white_paths and request.path != '/wechat/wxnotifyurl' and request.path is not '/' and not re.match(
#                 r'/swagger.*', request.path, re.I) and not re.match(r'/redoc/.*', request.path, re.I) and not re.match(
#                 r'/export.*', request.path, re.I):
#             print('查看authkey', request.META.get('HTTP_AUTHKEY'))
#             auth_key = request.META.get('HTTP_AUTHKEY')
#             # if auth_key:
#             #     print('查看秘钥：',cache.get(auth_key))
#             #     if cache.get(auth_key):
#             #         return JsonResponse({"message": "非法访问！已禁止操作！" , "errorCode": 10, "data": {}})
#             #     cache.set(auth_key, "true", timeout=60)
#             # else:
#             #     return JsonResponse({"message": "非法访问！已禁止操作！" , "errorCode": 10, "data": {}})


class learnAOP(MiddlewareMixin):
    def process_request(self, request):
        print('哈哈哈哈哈哈哈我是中间件request的路径:', request.META.get('REMOTE_ADDR'))