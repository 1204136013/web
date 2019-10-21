from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory,
)
import uuid
import os
from routes.helper import login_required
from models.user import User
from models.topic import Topic
from models.reply import Reply
from utils import (
    log,
    get_href,
)

main = Blueprint('index', __name__)


def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    u = User.one(id=uid)
    return u


"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    # form = request.args
    form = request.form
    print('testregister', form) 
    # 用类函数来判断
    u = User.register(form)
    if u == None:
        abort(404)
    else:
        return redirect(url_for('422_topic.index'))

@main.route("/getregister", methods=['GET'])
def getregister():
    # form = request.args
    # form = request.form
    # 用类函数来判断
    # u = User.register(form)
    basehref = get_href()
    return render_template("register.html", basehref=basehref)


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    print('login user <{}>'.format(u))
    if u is None:
        # 转到 topic.index 页面
        return redirect(url_for('.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('422_topic.index'))

@main.route("/getlogin", methods=['GET'])
def getlogin():
    # form = request.args
    # form = request.form
    # 用类函数来判断
    # u = User.register(form)
    basehref = get_href()
    return render_template("login.html", basehref=basehref)




# @main.route('/profile')
# def profile():
#     u = current_user()
#     if u is None:
#         return redirect(url_for('.index'))
#     else:
#         return render_template('profile.html', user=u)


# @main.route('/user/<int:id>')
# def user_detail(id):
#     u = User.one(id=id)
#     if u is None:
#         abort(404)
#     else:
#         return render_template('profile.html', user=u)


@login_required
@main.route('/user/<name>')
def user_detail(name):
    u = User.one(username = name)
    if u is None:
        abort(404)
    else:
        t = Topic.all(user_id = u.id)
        r = Reply.all(user_id = u.id)
        rt = []
        for x in r:
            topic = Topic.one(id = x.topic_id)
            if topic not in rt:   
                rt.append(topic)
        rt.sort(key=lambda x : x.updated_time)
        return render_template('profile.html', user=u, mytopic=t, othertopic = rt)


@main.route('/image/add', methods=['POST'])
def avatar_add():
    file: FileStorage = request.files['avatar']

    # filename = file.filename
    # ../../root/.ssh/authorized_keys
    # images/../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('.user_detail', name=u.username))


@main.route('/images/<filename>')
def image(filename):
    # 不要直接拼接路由，不安全，比如
    # http://localhost:2000/images/..%5Capp.py
    # path = os.path.join('images', filename)
    # print('images path', path)
    # return open(path, 'rb').read()
    # if filename in os.listdir('images'):
    #     return
    log('caonima', filename)
    return send_from_directory('images', filename)


@main.route("/todo")
def todo():
    u = current_user()
    return render_template("todo.html", user=u)

def not_found(e):
    return render_template('404.html')


# def blueprint():
#     main = Blueprint('index', __name__)
#     main.route("/")(index)
#     main.route("/register", methods=['POST'])(register)
#     main.route("/login", methods=['POST'])(login)
#     main.route('/profile')(profile)
#     main.route('/user/<int:id>')(user_detail)
#
#     return main
