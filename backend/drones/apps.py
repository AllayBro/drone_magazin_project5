from django.apps import AppConfig

class DronesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drones'
    
    def ready(self):
        """
        Метод для выполнения кода при инициализации приложения.
        Можно использовать для регистрации сигналов и т.д.
        """
        # import drones.signals  # Раскомментировать, если будут сигналы
        pass