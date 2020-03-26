#首先安装sdk库   pip install aliyun-python-sdk-core-v3
import json
import random

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

def create_code():
    #生成随机验证码
    base_str = '123456789123456789'
    return ''.join(random.sample(base_str, 4))



class SendSmsObject:
    def __init__(self, key, secret, region):
        self.key = key
        self.secret = secret
        self.region = region


    def get_template_param(self, **kwargs):
        return json.dumps(kwargs)

    def send_code(self, code_temp, mobile, code):
        client = AcsClient(self.key, self.secret, self.region)
        #key就是你的accessKeyId，secret就是你的accessSecret，'default

        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        #以上都是固定的
        request.set_action_name('SendSms')
       # set_action_name 这个是选择你调用的接口的名称，如：SendSms，SendBatchSms等


        request.add_query_param('RegionId', self.region)
        request.add_query_param('SignName', '劲诚科技')
        request.add_query_param('TemplateCode', code_temp)
        request.add_query_param('PhoneNumbers', mobile)
        request.add_query_param('TemplateParam', self.get_template_param(code=code))
        response = client.do_action_with_exception(request)
        return json.loads(response.decode('utf-8'))

    # request.add_query_param('PhoneNumbers', "13222222222")  # 发给谁
    # request.add_query_param('SignName', "博客")  # 签名
    # request.add_query_param('TemplateCode', "SMS_111111111")  # 模板编号
    # request.add_query_param('TemplateParam', f"{template}")  # 发送验证码内容
    # response = client.do_action_with_exception(request)
    # print(str(response, encoding='utf-8'))

