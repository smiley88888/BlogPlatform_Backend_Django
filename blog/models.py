from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from django.conf import settings

Base = declarative_base()

engine = create_engine(f'mysql+pymysql://{settings.DATABASES["default"]["USER"]}:{settings.DATABASES["default"]["PASSWORD"]}@{settings.DATABASES["default"]["HOST"]}/{settings.DATABASES["default"]["NAME"]}')
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(Text)
    user = relationship("User", back_populates="posts")

User.posts = relationship("Post", order_by=Post.id, back_populates="user")

Base.metadata.create_all(engine)