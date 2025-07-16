from django.apps import AppConfig


class AppsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps'

    def ready(self):
        from apps.models import User
        import apps.signals

        SUPER_PHONE = 'admin@gmail.com'
        SUPER_PASS = '1'

        try:
            if not User.objects.filter(email=SUPER_PHONE).exists():
                User.objects.create_superuser(
                    email=SUPER_PHONE,
                    password=SUPER_PASS,
                    is_staff=True,
                    is_superuser=True
                )
                print(f"✅ Superuser created: {SUPER_PHONE}")
            else:
                print("ℹ️ Superuser already exists.")
        except Exception as e:
            print(f"⚠️ Superuser creation skipped: {e}")
