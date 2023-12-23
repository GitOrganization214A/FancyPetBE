from django.apps import AppConfig
from django.db.backends.signals import connection_created
from django.dispatch import receiver


class FancypetConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "FancyPet"

    def ready(self):
        connection_created.connect(self.configure_db)

    def configure_db(self, sender, connection, **kwargs):
        # 设置连接的字符集为 utf8mb4
        with connection.cursor() as cursor:
            cursor.execute('SET NAMES utf8mb4')
