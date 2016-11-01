from models import *
from models.blog_model import Blog


class Comment(db.Model, ModelMixin):
    __tablename__ = 'comments'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(30))
    created_time = db.Column(db.String(30))

    # 定义外键字段
    user_id = db.Column(db.String(30), db.ForeignKey('users.username'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))

    def __init__(self, form):
        self.content = form.get('content', '')
        self.blog_id = form.get('blog_id', '')
        self.created_time = format_time(int(time.time()))

    def to_dict(self):
        d = {
            'id': self.id,
            'content': self.content,
            'created_time': self.created_time,
            'user_id': self.user_id,
            'blog_id': self.blog_id,
        }
        return d

    def comment_valid(self):
        if len(self.content) == 0:
            return False, None, '评论不能为空'
        elif len(self.content) > 30:
            return False, None, '评论不能超过30字'
        else:
            self.comment_counter(self.blog_id)
            self.save()
            return True, self.to_dict(), '评论成功'

    def comment_counter(self, bid):
        b = Blog.query.get(bid)
        b.comment_count += 1
        b.save()
