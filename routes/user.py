from routes import *


main = Blueprint('user', __name__)


@main.route('/')
def login_view():
    return render_template('login.html')


@main.route('/user/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    if u.valid_register():
        u.hash_password(u.password)
        u.save()
    else:
        return abort(404)
    return redirect(url_for('user.login_view'))


@main.route('/user/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    user = User.query.filter_by(username=u.username).first()
    if user is not None and user.valid_login(u):
        session['user_id'] = user.id
    else:
        print('登录失败')
        return redirect(url_for('.login_view'))
    return redirect(url_for('blog.user_index', username=user.username))


@login_required
@main.route('/user/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('.login_view'))
