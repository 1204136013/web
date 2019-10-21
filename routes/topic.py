from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import current_user
from routes.helper import current_user, csrf_required, new_csrf_token, login_required, csrf_tokens, sameuser_required

from models.topic import Topic


main = Blueprint('422_topic', __name__)


@main.route("/")
def index():
    ms = Topic.all()
    u = current_user()
    token = new_csrf_token()
    return render_template("topic/index.html", ms=ms, user=u, token=token)


@main.route('/<int:id>')
# /topic/1
# @main.route('/')
# /topic?id=1
# zhihu.com/question/1/answer/2/comment/3/xxx/y
def detail(id):
    # id = int(request.args['id'])
    # http://localhost:3000/topic/1
    # m = Topic.one(id=id)
    m = Topic.get(id)
    u = current_user()
    # 不应该放在路由里面
    # m.views += 1
    # m.save()
    token = new_csrf_token()
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m, token=token, user=u)


@main.route("/add", methods=["POST"])
@login_required
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    m = Topic.add(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
@login_required
@csrf_required
def delete():
    u = current_user()

    # token = request.args['token']
    # user_id = csrf_tokens[token]
    # assert user_id == u.id
    user = request.args['user']
    id = int(request.args['id'])
    print('删除 topic 用户是', u, id)
    if u.username == user:
        Topic.delete(id)
    return redirect(url_for('.index'))



@main.route("/new")
def new():
    return render_template("topic/new.html")

