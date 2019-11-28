from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from search import add_to_index, remove_from_index, query_index, create_index

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

    @classmethod
    def create_es_index(cls):
    	create_index()


class Measurable(SearchableMixin, db.Model):
	__searchable__ = ['name', 'description']
	__tablename__ = 'measurables'

	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80))
	description = db.Column(db.Text())
	modality = db.Column(db.String(80))

class Modality(SearchableMixin, db.Model):
	__searchable__ = ['name', 'description']
	__tablename__ = 'modalities'

	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80))
	description = db.Column(db.Text())

class Technology(SearchableMixin, db.Model):
	__searchable__ = ['name', 'manufacturer', 'description','short_description']
	__tablename__ = 'technologies'

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

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)
@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))



