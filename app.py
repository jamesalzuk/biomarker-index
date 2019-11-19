import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_restful import Api
import requests
import pandas as pd

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)



app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

from auth import UserLogin, UserRegister
from models import Modality, Measurable, Technology

api.add_resource(UserRegister, '/auth/register')
api.add_resource(UserLogin, '/auth/login')

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		data={'email': request.form['email'],
		'password': request.form['password']}
		print(data)
		r = requests.post(
			url="http://localhost:5000/auth/login",
			data=data
			)

		print(r.json())
	return render_template('login.html')



@app.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('email', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@app.route('/', methods=['GET', 'POST'])
@jwt_required
def index():
	return render_template('index.html')

@app.route('/measurable', methods=['GET', 'POST'])
def measurable_list():
	measurables = []
	if request.method == 'POST':
		name = request.form['measurable']
		m = Measurable.query.filter_by(name=name).first()
		measurables.append(m)
	else:
		measurables = Measurable.query.all()
	return render_template('measurable_list.html', measurables=measurables)

@app.route('/technology', methods=['GET', 'POST'])
def technology_list():
	technologies = []
	if request.method == 'POST':
		name = request.form['technology']
		t = Technology.query.filter_by(name=name).first()
		technologies.append(t)
	else:
		technologies = Technology.query.all()
	return render_template('technology_list.html', technologies=technologies)

@app.route('/modality', methods=['GET', 'POST'])
def modality_list():
	modalities = []
	if request.method == 'POST':
		name = request.form['modality']
		m = Modality.query.filter_by(name=name).first()
		modalities.append(m)
	else:
		modalities = Modality.query.all()
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

