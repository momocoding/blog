from flask import Flask
from flask import render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from models import db


# 这里 import 具体的 Model 类是为了给 migrate 用
# 如果不 import 那么无法迁移
# 这是 SQLAlchemy 的机制
from models import user_model
from models import blog_model
from models import comment_model

# 导入各个路由蓝图
from routes.user import main as user_routes
from routes.api import main as api_routes
from routes.blog import main as blog_routes


app = Flask(__name__)
db_path = 'demo.sqlite'
manager = Manager(app)


def register_routes():
    app.register_blueprint(user_routes)
    app.register_blueprint(api_routes, url_prefix='/api')
    app.register_blueprint(blog_routes, url_prefix='/blog')


def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'secret key'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/blog?charset=utf8'
    db.init_app(app)
    register_routes()


def configured_app():
    configure_app()
    return app


@manager.command
def server():
    app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)
    ...


def configure_manager():
    # 配置命令行选项
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


@app.errorhandler(404)
def error404(e):
    return render_template('404.html')


if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()

