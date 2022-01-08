# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from databank import create_app, db
from datetime import datetime
from databank.models import User, PersonData, Location

app = create_app('testing')

with app.app_context():
    db.drop_all()
    db.create_all()
    born_time = datetime(1995, 7, 18, 23, 45)
    location = Location(country="china", timezone="+8", latitude="E188", longtitude="N23", city="奉新")
    db.session.add(location)
    db.session.commit()
    person = PersonData(name="stella", gender=0, location_id=1, born_time=born_time, belong_user=1)
    db.session.add(person)
    db.session.commit()

    # user = User(username='grey')
    # user.set_password('123')
    # db.session.add(user)
    #
    # item1 = Item(body='test item 1')
    # item2 = Item(body='test item 2')
    # item3 = Item(body='test item 3')
    # item4 = Item(body='test item 4', done=True)
    # user.items = [item1, item2, item3, item4]
    #
    # db.session.commit()
