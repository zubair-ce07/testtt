from exceptions import AttributeNotFound, ImproperlyConfigured
from importlib import import_module

import database_handler
from utils import get_settings
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request
from werkzeug.wsgi import SharedDataMiddleware


def run_server():
    intialize_database()
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple(
        '127.0.0.1',
        5000,
        app,
        use_debugger=True,
        use_reloader=True
    )


class Framework:
    def __init__(self):
        settings = get_settings()
        try:
            self.view_controllers = import_module(settings.view_controllers)
            self.url_mapping = import_module(settings.url_mapping)
        except ImportError as exc:
            raise ImproperlyConfigured(exc)

        self.create_url_rules()

    def create_url_rules(self):
        try:
            url_rules = self.url_mapping.url_rules
        except AttributeError:
            raise AttributeNotFound(
                "Module {0} : has not set attribute url_rules".format(
                    self.url_mapping
                ))

        self.url_map = Map([Rule(rule, endpoint=endpoint)
                            for rule, endpoint in url_rules.items()])

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self.view_controllers, endpoint)(request, **values)
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app():
    settings = get_settings()
    app = Framework()
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/static':  settings.static_path
    })
    return app


def intialize_database():
    settings = get_settings()
    if hasattr(settings, "DB_URL"):
        if hasattr(settings, "DB_MODELS"):
            database_handler.intialize_database()
