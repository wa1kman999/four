from qiniu import Auth, put_data

from four import settings


q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
def get_token(filename):
    # if classifcation == 'img':
    bucket_name = 'walkmanstore'
    # else:
    #     bucket_name = '11111'   #要上传的空间
    key = None      #上传后保存的文件名
    policy = {                         #上传文件到七牛后， 七牛将文件名和文件大小回调给业务服务器。
     # 'callbackUrl': settings.SELF_HOST + 'api/v1/users/callback',
        'callbackUrl': settings.SELF_HOST + 'api/v1/users/callback',
        'callbackBody': 'filename=$(fname)&filesize=$(fsize)&uuid=%s' % filename
     }
    token = q.upload_token(bucket_name, key, 3600, policy)   #生成上传 Token，可以指定过期时间等
    return token


def upload_avatar(filename, data):
    key = filename
    token = get_token(filename)
    put_data(token, key, data)
    avatar_url = 'http://q8goto9jq.bkt.clouddn.com/' + filename
    return avatar_url
