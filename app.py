import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
import requests
import pandas as pd



app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Modality, Measurable, Technology 

@app.route('/', methods=['GET', 'POST'])
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
	db.drop_all()
	db.session.commit()
	return 200, "OK"
#@app.route('/technology/<id>')
#def modality(id):
#	modality=Measurable.query.all()[0].modality
#	measurables=Measurable.query.filter_by(modality=modality)
#	return render_template('modality.html', measurables=measurables, modality=modality)


if __name__ == '__main__':
	print(os.environ['APP_SETTINGS'])
	print(app.config)
	app.run()

