from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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

class User(UserMixin, db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(256),nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))



