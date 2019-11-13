import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
import requests



app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Modality, Measurable 

@app.route('/', methods=['GET', 'POST'])
def index():
	measurables = []
	if request.method == 'POST':
		name = request.form['measurable']
		m = Measurable.query.filter_by(name=name).first()
		measurables.append(m)
	else:
		measurables = Measurable.query.all()
	return render_template('index.html', measurables=measurables)

@app.route('/modality/<id>')
def modality(id):
	modality=Measurable.query.all()[0].modality
	measurables=Measurable.query.filter_by(modality=modality)
	return render_template('modality.html', measurables=measurables, modality=modality)

#@app.route('/technology/<id>')
#def modality(id):
#	modality=Measurable.query.all()[0].modality
#	measurables=Measurable.query.filter_by(modality=modality)
#	return render_template('modality.html', measurables=measurables, modality=modality)


if __name__ == '__main__':
	print(os.environ['APP_SETTINGS'])
	print(app.config)
	app.run()

