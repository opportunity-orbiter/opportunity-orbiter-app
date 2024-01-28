from django.conf import settings


def global_settings(request):
    return {"PROJECT_NAME": settings.PROJECT_NAME, "OPENAI_KEY": settings.OPENAI_KEY}
