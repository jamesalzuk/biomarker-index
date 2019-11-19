from app import db

class Measurable(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80))
	description = db.Column(db.Text())
	modality = db.Column(db.String(80))

class Modality(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80))
	description = db.Column(db.Text())

class Technology(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80))
	manufacturer = db.Column(db.String(80))
	url = db.Column(db.String(240))
	short_description=db.Column(db.Text())
	description = db.Column(db.Text())
	passive	= db.Column(db.Boolean())
	portable = db.Column(db.Boolean())
	wearing_position = db.Column(db.String(80))
	open_source = db.Column(db.Boolean())
	sdk_api	= db.Column(db.Boolean())
	raw_data_access	= db.Column(db.Boolean())
	minimum_cost_gbp = db.Column(db.Float())
	maximum_cost_gbp = db.Column(db.Float())
	availability = db.Column(db.String(80))
	clinical_validation	= db.Column(db.String(80))
	medical_approval = db.Column(db.String(80))	
	self_administer = db.Column(db.String(80))
	compatibility = db.Column(db.String(80))
		
# project/server/models.py

import jwt
import datetime

from app import app, db


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

