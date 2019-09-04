from rest_framework import routers

# https://stackoverflow.com/questions/31483282/django-rest-framework-combining-routers-from-different-apps


class DefaultRouter(routers.DefaultRouter):
    def extend(self, router):
        self.registry.extend(router.registry)
