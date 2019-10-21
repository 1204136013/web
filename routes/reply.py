from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
)
from routes.helper import login_required
from routes import current_user

from models.reply import Reply


main = Blueprint('422_reply', __name__)


@main.route("/add", methods=["POST"])
@login_required
def add():
    form = request.form.to_dict()
    u = current_user()
    print('DEBUG', form)
    m = Reply.add(form, user_id=u.id)
    return redirect(url_for('422_topic.detail', id=m.topic_id))

