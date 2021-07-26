import django.dispatch

Part_Saved = django.dispatch.Signal(providing_args=["title"])