from models import *
from models.user_model import User
from markdown import markdown


class Blog(db.Model, ModelMixin):
    __tablename__ = 'blogs'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    read_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    title = db.Column(db.String(50))
    sort = db.Column(db.String(20))
    summary = db.Column(db.String(150))
    content = db.Column(db.String(1000))
    created_time = db.Column(db.String(30))

    # 定义外键关系
    user_id = db.Column(db.String(30), db.ForeignKey('users.username'))
    comments = db.relationship('Comment', backref='blog')

    def __init__(self, form):
        self.title = form.get('title', '')
        self.sort = form.get('sort', '')
        self.comment_count = 0
        self.read_count = 0
        self.summary = form.get('summary', '')
        self.content = form.get('content', '')
        self.created_time = format_time(int(time.time()))
        self.user_avatar = ''

    def to_dict(self):
        d = {
            'id': self.id,
            'sort': self.sort,
            'title': self.title,
            'comment_count': self.comment_count,
            'read_count': self.read_count,
            'summary': self.summary,
            'content': self.content,
            'created_time': self.created_time,
            'user_id': self.user_id,
            # 'comments': self.comments,
        }
        return d

    def summary_handle(self):
        if self.summary == '':
            if len(self.content) > 150:
                # self.summary = markdown(self.content[:150])
                self.summary = self.content[:150] + '...'
            else:
                # self.summary = markdown(self.content)
                self.summary = self.content + '...'

    def load_avatar(self):
        self.user_avatar = User.query.filter_by(username=self.user_id).first().avatar

    def update(self, form):
        if self.title != form['title']:
            self.title = form['title']
        if self.summary != form['summary']:
            self.summary = form['summary']
        if self.content != form['content']:
            self.content = form['content']
        if self.sort != form['sort']:
            self.sort = form['sort']

    def blog_delete(self, current):
        if self.user_id == current.username or current.id == 1:
            self.delete()
            return True, '删除成功'
        else:
            return False, '删除失败'

    def blog_valid(self):
        if len(self.title) == 0 or len(self.content) == 0:
            return False, None, '标题和内容不能为空'
        elif len(self.title) > 50:
            return False, None, '标题不能超过50字'
        else:
            self.save()
            return True, self.to_dict(), '提交成功'
