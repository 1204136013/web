import time

from sqlalchemy import String, Column, Integer, UnicodeText

from models import Model
from models.base_model import db, SQLMixin
from models.user import User
# from models.topic import Topic

class Reply(SQLMixin, db.Model):

    content = Column(UnicodeText, nullable=False)
    topic_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    def user(self):
        u = User.one(id=self.user_id)
        return u

    @classmethod
    def add(self, form, user_id):

        from models.topic import Topic
        t_id = form['topic_id']
        t = Topic.one(id=t_id)
        t.update(t_id, updated_time=time.time())
        # t.updated_time = time.time()

        form['user_id'] = user_id
        r = Reply.new(form)
        return r


