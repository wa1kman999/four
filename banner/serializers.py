from .models import FriendLink, Banner, Activity
from rest_framework import serializers


class FriendLinkViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendLink
        exclude = ('created')


class BannerViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        exclude = ('level', 'created')


class ActivityViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"

