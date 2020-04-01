from datetime import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User
from django.db import transaction


@transaction.atomic   #事务 保障操作在一个事务中
@receiver(post_save, sender=User)
def create_update_object(sender, instance, created=False, **kwargs):
    '''
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    '''
    print('对象保存时 signals流转详情：')
    print(sender)
    if created:
        print('新增时：', instance)
        print('新增时：', instance.email)

    else:
        print('修改时：', instance)


@transaction.atomic
@receiver(post_delete, sender=User)
def delete_object(sender, instance=None, **kwargs):
    '''
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    '''
    print('对象删除时 查看signals流转详情：')
    print(sender)
    print('被删除的')