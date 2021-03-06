import time
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from events import socketio
import config

# web framework
# web application
# __main__
import secret
from models.base_model import db
from models.reply import Reply
from models.topic import Topic
from models.user import User
from routes import index
from utils import log

# 注册蓝图
# 有一个 url_prefix 可以用来给蓝图中的每个路由加一个前缀
# import routes.index as index_view
from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.index import not_found
from routes.chat import main as chat_routes

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# db = SQLAlchemy(app)


class UserModelView(ModelView):
    column_searchable_list = ('username', 'password')


# @app.template_filter()
def count(input):
    log('count using jinja filter')
    return len(input)


def format_time(unix_timestamp):
    # enum Year():
    #     2013
    #     13
    # f = Year.2013
    f = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(unix_timestamp)
    formatted = time.strftime(f, value)
    return formatted


def configured_app():
    app = Flask(__name__)
    # 设置 secret_key 来使用 flask 自带的 session
    # 这个字符串随便你设置什么内容都可以
    app.secret_key = config.secret_key

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost/web19?charset=utf8mb4'.format(
        secret.database_password
    )
    db.init_app(app)


    # module = __import__('routes.index')
    # b = getattr(getattr(module, 'index'), 'blueprint')()
    # log('index blueprint', b)
    # app.register_blueprint(b)
    # log('url map', app.url_map)
    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(chat_routes, url_prefix='/chat')

    app.template_filter()(count)
    app.template_filter()(format_time)
    app.errorhandler(404)(not_found)

    admin = Admin(app, name='web19', template_mode='bootstrap3')
    mv = UserModelView(User, db.session)
    mv.column_searchable_list = ['username', 'password']
    admin.add_view(mv)

    # admin.add_view(ModelView(User, db.session))
    # admin.add_view(ModelView(Topic, db.session))
    # admin.add_view(ModelView(Reply, db.session))
    # Add administrative views here
    socketio.init_app(app)

    return app


# 运行代码
if __name__ == '__main__':
    # app.add_template_filter(count)
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    # 自动 reload jinja
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=3000,
        # ssl_context='adhoc',
    )
    # app.run(**config)
    socketio.run(app, **config)

