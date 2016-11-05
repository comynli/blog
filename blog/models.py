from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from m.extensions.sqlalchemy import SQLAlchemy


db = SQLAlchemy(config_prefix='database')


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(45), unique=True, nullable=False)
    mail = Column(String(64), unique=True, nullable=False)
    password = Column(String(64), nullable=False)

    catalogs = relationship('Catalog', foreign_keys='[Catalog.user_id]')


class Catalog(db.Model):
    __tablename__ = 'catalog'
    __table_args__ = (UniqueConstraint('user_id', 'name', name='uq_catalog_user_name'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String(45), nullable=False)


class Post(db.Model):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(192), nullable=False, default='new post')
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    catalog_id = Column(Integer, ForeignKey('catalog.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    status = Column(Integer, nullable=False, default=0)
    read_count = Column(Integer, nullable=False, default=0)
    image = Column(String(256), nullable=True)

    author = relationship('User', foreign_keys=[author_id])
    catalog = relationship('Catalog', foreign_keys=[catalog_id])
    content = relationship('PostContent', foreign_keys='[PostContent.id]', uselist=False)


class PostContent(db.Model):
    __tablename__ = 'post_content'

    id = Column(Integer, ForeignKey('post.id'), primary_key=True)
    content = Column(Text, nullable=False)


class Favorite(db.Model):
    __tablename__ = 'favorite'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), primary_key=True)


class Like(db.Model):
    __tablename__ = 'like'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), primary_key=True)


class Comment(db.Model):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    ref_id = Column(Integer, ForeignKey('comment.id'), nullable=True)
    content = Column(String(420), nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)

    user = relationship('User', foreign_keys=[user_id])
    ref = relationship('Comment', foreign_keys=[ref_id], uselist=False)
