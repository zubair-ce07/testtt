from flask import Blueprint, Response
from scraper.scraper.deBijenkorfScraper import UpdatedProgress
bp = Blueprint('update_progress', __name__)


@bp.route('/progress')
def progress():
    def import_progress():
        yield "data:" + str(UpdatedProgress.get_count()) + "\n\n"
    return Response(import_progress(), mimetype='text/event-stream')

