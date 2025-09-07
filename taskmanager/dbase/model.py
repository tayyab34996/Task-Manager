from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
from datetime import datetime
Base= declarative_base()
class NewUser(Base, UserMixin):
    __tablename__='Users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username=Column(String(32),nullable=False, unique=True)
    fullname= Column(String(32), nullable=False)
    dateofBirth = Column(String(32), nullable=True)
    gender = Column(String(10), nullable=True)
    address = Column(String(128), nullable=True)
    profilePicture = Column(String, nullable=True)
    about_me = Column(String(256), nullable=True)
    email = Column(String(32), nullable=False, unique=True)
    password = Column(String(32), nullable=False)
    
    def __repr__(self):
        return f"<NewUser(username={self.username}, fullname={self.fullname}, email={self.email}, password={self.password})>"
    def verify_password(self, password):
        return self.password == password
class Task(Base):
    __tablename__ = 'Tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    user = Column(String, nullable=False)
    date = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(String, nullable=False)
    status = Column(String, nullable=False, default='pending')
    def __repr__(self):
        return f"<Task(title={self.title}, user={self.user}, date={self.date}, priority={self.priority}, status={self.status})>"