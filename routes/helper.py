import functools
import uuid
from functools import wraps

from flask import session, request, abort, redirect, url_for

from models.user import User
from utils import log


def login_required(route_function):

    @functools.wraps(route_function)
    def f():
        log('login_required')
        u = current_user()
        if u is None:
            log('游客用户')
            return redirect(url_for('index.index'))
        else:
            log('登录用户', route_function)
            return route_function()

    return f


def sameuser_required(route_function):

    @functools.wraps(route_function)
    def f(a):
        log('login_required')
        u = current_user()
        if u is None:
            log('游客用户')
            return redirect(url_for('index.index'))
        else:
            log('登录用户', route_function)
            return route_function(a)

    return f


def current_user():
    uid = session.get('user_id', '')
    u: User = User.one(id=uid)
    # type annotation
    # User u = User.one(id=uid)
    return u


csrf_tokens = dict()


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        log('csrf_user', '1', token, '2', u.username, '3', csrf_tokens)
        if token in csrf_tokens and csrf_tokens[token] == u.id:
            csrf_tokens.pop(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    if u==None:
        csrf_tokens[token] = -1
    else:
        csrf_tokens[token] = u.id
    return token
