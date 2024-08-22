from django.apps import AppConfig


class SupportConfig(AppConfig):
    name = 'support_question'

    def ready(self):
        import support_question.receivers
