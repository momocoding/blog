from routes import *


main = Blueprint('api', __name__)


# 验证登陆装饰器
def api_login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            r = response(302, message='请登录之后评论')
            return r
        return f(*args, **kwargs)
    return function


# 添加blog
@admin_required
@main.route('/blog/add', methods=['POST'])
def blog_add():
    u = current_user()
    form = request.form
    b = Blog(form)
    b.summary_handle()
    # b.content = markdown(b.content)
    b.user_id = u.username
    status, data, message = b.blog_valid()
    r = response(status, data, message)
    return r


# 添加评论
@main.route('/comment/add', methods=['POST'])
@api_login_required
def comment_add():
    u = current_user()
    form = request.form
    c = Comment(form)
    c.user_id = u.username
    status, data, message = c.comment_valid()
    r = response(status, data, message)
    return r


# 更新blog
@main.route('/blog/update/<int:id>', methods=['POST'])
def blog_update(id):
    form = request.form
    b = Blog.query.get(id)
    b.update(form)
    b.summary_handle()
    status, data, message = b.blog_valid()
    # log('response', status, data, message)
    r = response(status, data=data, message=message)
    return r


# 加载全文
@main.route('/blog/content', methods=['POST'])
def load_content():
    blog_id = request.form.get('id', '')
    b = Blog.query.get(blog_id)
    b.read_count += 1
    b.save()
    # r = response(True, data=b.content)
    r = response(True, data=md_to_html(b.content))
    # log('source', b.content)
    # log('md', md_to_html(b.content))
    return r


# 删除blog
@admin_required
@main.route('/blog/delete/<int:id>')
def blog_delete(id):
    current = current_user()
    b = Blog.query.get(id)
    status, message = b.blog_delete(current)
    r = response(status, message=message)
    return r












