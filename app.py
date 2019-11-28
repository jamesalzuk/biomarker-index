import os, re
from flask import Flask, render_template, request, jsonify, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse
import requests
import pandas as pd
from datetime import datetime
from elasticsearch_instance import es

# Verify that Python can talk to Bonsai (optional):

app = Flask(__name__)
app.elasticsearch = es
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import Modality, Measurable, Technology, User
from forms import LoginForm, RegistrationForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, registered_on=datetime.now(), admin=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route('/measurable', methods=['GET', 'POST'])
def measurable_list():
	measurables = []
	if request.args:
		args=request.args
		query = args['search']
		measurables, number = Measurable.search(query,1,10)
	return render_template('measurable_list.html', measurables=measurables)

@app.route('/technology', methods=['GET', 'POST'])
def technology_list():
	technologies = []
	if request.args:
		args=request.args
		query = args['search']
		technologies, number =  Technology.search(query, 1,10)
	return render_template('technology_list.html', technologies=technologies)

@app.route('/modality', methods=['GET', 'POST'])
def modality_list():
	modalities = []
	if request.args:
		args=request.args
		query = args['search']
		modalities, number = Modality.search(query, 1,10)

	return render_template('modality_list.html', modalities=modalities)

@app.route('/modality/<id>')
def modality(id):
	modality=Measurable.query.all()[0].modality
	measurables=Measurable.query.filter_by(modality=modality)
	return render_template('modality.html', measurables=measurables, modality=modality)

@app.route('/import')
def data_import():
	if not Modality.query.all():
		df = pd.read_csv('modalities.csv',sep='|')
		db.session.bulk_insert_mappings(Modality,df.to_dict(orient="records"))
	if not Technology.query.all():
		df = pd.read_csv('technologies.csv',sep='|')
		db.session.bulk_insert_mappings(Technology,df.to_dict(orient="records"))
	if not Measurable.query.all():
		df = pd.read_csv('measurables.csv',sep='|')
		db.session.bulk_insert_mappings(Measurable,df.to_dict(orient="records"))
	db.session.commit()
	return 200, "OK"

@app.route('/drop')
def drop():
	db.session.execute('DROP TABLE alembic_version;')
	db.drop_all()
	db.session.commit()
	return 200, "OK"

@app.route('/technology/<id>')
def technology(id):
	modality=Measurable.query.all()[0].modality
	measurables=Measurable.query.filter_by(modality=modality)
	return render_template('modality.html', measurables=measurables, modality=modality)


if __name__ == '__main__':
	print(os.environ['APP_SETTINGS'])
	print(app.config)
	app.run()

