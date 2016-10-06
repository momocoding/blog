from routes import *
from sqlalchemy import desc


main = Blueprint('blog', __name__)


@main.route('/<username>')
def user_index(username):
    current = current_user()
    # status = False
    # if cu is not None:
    #     if cu.username == username:
    #         status = True
    #     current = cu
    # else:
    #     current = '游客'
    #
    # if username == '游客':
    #     return redirect(url_for('user.login_view'))
    u = User.query.filter_by(username=username).first()
    if u is None:
        abort(404)
    else:
        blogs = Blog.query.filter_by(user_id=username).order_by('created_time desc').all()
        for b in blogs:
            b.load_avatar()
            b.summary = md_to_html(b.summary)
        return render_template('blog_index.html', blogs=blogs, current=current, tops=None)


@main.route('/')
def all():
    # 查找所有的 blog 并返回
    current = current_user()
    blogs = Blog.query.order_by('created_time desc').all()
    # tops = Blog.query.order_by('read_count desc').limit(10).offset(0)
    tops = Blog.query.order_by(desc(Blog.read_count)).limit(10).offset(0)
    # for t in tops:
    #     log('标题', t.read_count, t.title)
    for b in blogs:
        b.load_avatar()
        # b.content = markdown(b.content)
        b.summary = md_to_html(b.summary)
    return render_template('blog_index.html', blogs=blogs, current=current, tops=tops)


@main.route('/add')
@admin_required
@login_required
def add_view():
    current = current_user()
    return render_template('add_view.html', current=current)


@main.route('/edit/<int:id>')
@admin_required
@login_required
def edit_view(id):
    current = current_user()
    b = Blog.query.get(id)
    return render_template('edit_view.html', current=current, blog=b)


# @main.route('/update/<int:id>', methods=['POST', 'GET'])
# def update(id):
#     current = current_user()
#     b = Blog.query.get(id)
#     form = request.form
#     b.update(form)
#     log('11111')
#     return redirect(url_for('.user_index', username=current.username))








