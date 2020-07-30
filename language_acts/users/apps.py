from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "language_acts.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import language_acts.users.signals  # noqa F401
        except ImportError:
            pass
