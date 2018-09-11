from jinja2 import Environment, FileSystemLoader

from utils import get_settings
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

settings = get_settings()
templates_env = Environment(loader=FileSystemLoader(
        settings.template_path),
        autoescape=True
    )


def render_template(template_name, **context):
    template = templates_env.get_template(template_name)
    return Response(template.render(context), mimetype='text/html')


def redirect_to_path(path):
    return redirect("/")
