import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Class(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'classes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    timetable = sqlalchemy.Column(sqlalchemy.String)
    tg_s = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    changed_lessons = sqlalchemy.Column(sqlalchemy.String, nullable=True)
