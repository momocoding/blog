from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import abort
from flask import session
from functools import wraps
from markdown import markdown
import bleach
import json

from models.user_model import User
from models.blog_model import Blog
from models.comment_model import Comment


def log(*args):
    print(*args)


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


def response(success, data=None, message=''):
    r = dict(
        success=success,
        data=data,
        message=message,
    )
    return json.dumps(r, ensure_ascii=False)


# 所装饰的函数如果有return, 调用之后也应该return 该函数
def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('user.login_view'))
        return f(*args, **kwargs)
    return function


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user().id != 1:
            return redirect(url_for('blog.all'))
        return f(*args, **kwargs)
    return function


# markdown处理
# 允许的标签
allow_tags = [
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'code',
    'em',
    'i',
    'li',
    'ol',
    'pre',
    'strong',
    'ul',
    'h1',
    'h2',
    'h3',
    'p',
    'img',
]

# 允许的属性,这样设置将不会过滤所有标签的class属性,和a标签的href,rel属性....
allow_attrs = {
    '*': ['class'],
    'a': ['href', 'rel'],
    'img': ['src', 'alt'],
}


def md_to_html(content):
    content = markdown(content, output_format='html')
    cleaned_html = bleach.clean(content, tags=allow_tags, strip=True, attributes=allow_attrs)
    return cleaned_html