from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    # Associate app with users.signals
    def ready(self):
        import users.signals