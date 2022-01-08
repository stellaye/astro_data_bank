# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from databank.extensions import db


class PersonData(db.Model, UserMixin):
    __tablename__ = "person_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, index=True)
    gender = db.Column(db.Integer)
    born_time = db.Column(db.DateTime)
    born_data_rate = db.Column(db.VARCHAR(10))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    tag = db.Column(db.Text)
    basic_info = db.Column(db.Text)
    history = db.Column(db.Text)
    status = db.Column(db.Integer)
    belong_user = db.Column(db.Integer, default=0)
    relation = db.Column(db.String(10))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Location(db.Model):
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String(10), default="中国")
    province = db.Column(db.String(10), default="江西")
    city = db.Column(db.String(10), default="奉新")
    longtitude = db.Column(db.String(10))
    latitude = db.Column(db.VARCHAR(10))
    timezone = db.Column(db.VARCHAR(4))


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10))
    username = db.Column(db.String(10))
    password = db.Column(db.String(6))
