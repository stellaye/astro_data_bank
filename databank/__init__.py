import os
from flask import Flask, render_template, jsonify, request
from databank.extensions import db
from databank.models import User, PersonData, Location
from databank.settings import config
from databank.blueprints.bazi import bazi_bp



def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('astro_bank')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(bazi_bp)
