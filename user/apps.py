from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'

 # 激活signals
    def ready(self):
        import user.signals
