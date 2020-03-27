# 频率组件
import time
from rest_framework.throttling import BaseThrottle
VISIT_RECORD = {}
class VisitThrottle(BaseThrottle):
    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        remote_addr = request.META.get('HTTP_X_REAL_IP')
        # print('请求的IP：',remote_addr)
        ctime = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [ctime,]
            return True
        history = VISIT_RECORD.get(remote_addr)
        self.history = history
        while history and history[-1] < ctime - 60:
            history.pop()
        if len(history) < 100:  # 限制的频数 设置同一IP该接口一分钟内只能被访问100次
            history.insert(0, ctime)
            return True
        else:
            return False

    def wait(self):
        ctime = time.time()
        return 60 - (ctime-self.history[-1])
