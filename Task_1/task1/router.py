from rest_framework.routers import Route, SimpleRouter


class ListReadOnlyRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={'get': 'list'},
            name='{basename}',
            initkwargs={'suffix': 'List'}
        )
    ]
