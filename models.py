# In your app's apps.py

from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'calculator'

    def ready(self):
        import calculator.signals # Ensure this path is correct