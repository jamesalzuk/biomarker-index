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
	url = db.Column(db.String(80))
	description = db.Column(db.Text())
	passive	= db.Column(db.Boolean())
	portable = db.Column(db.Boolean())
	wearing_position = db.Column(db.String(80))
	open_source = db.Column(db.Boolean())
	sdk	= db.Column(db.Boolean())
	raw_data_access	= db.Column(db.Boolean())
	minimum_cost_gbp = db.Column(db.Decimal())
	maximum_cost_gbp = db.Column(db.Decimal())
	availability = db.Column(db.String(80))
	clinical_validation	= db.Column(db.String(80))
	medical_approval = db.Column(db.String(80))	
	self_administer = db.Column(db.String(80))
	compatibility = db.Column(db.String(80))
		

	#measurables = 	
	#comments	
	#modalities covered	