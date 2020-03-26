from rest_framework import generics
from .serializers import FriendLinkViewSerializer, BannerViewSerializer, ActivityViewSerializer
from .models import FriendLink, Banner, Activity
from rest_framework.response import Response

class FriendLinkView(generics.GenericAPIView):
    serializer_class = FriendLinkViewSerializer
    def get(self, request):
        queryset = FriendLink.objects.all()
        serializer = self.serializer_class(instance=queryset, many=True)
        data = serializer.data
        return Response({'MSG': '获取信息成功', 'errorCode': 0, 'data': data})



class BannerView(generics.GenericAPIView):
    serializer_class = BannerViewSerializer
    def get(self, request):
        queryset = Banner.objects.all()
        serializer = self.serializer_class(instance=queryset, many=True)
        data = serializer.data
        return Response({'MSG': '获取信息成功', 'errorCode': 0, 'data': data})

class ActivityView(generics.GenericAPIView):
        serializer_class = ActivityViewSerializer

        def get(self, request):
            queryset = Activity.objects.all()
            serializer = self.serializer_class(instance=queryset, many=True)
            data = serializer.data
            return Response({'MSG': '获取信息成功', 'errorCode': 0, 'data': data})