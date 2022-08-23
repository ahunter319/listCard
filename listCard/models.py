from listCard import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    """Given user_id, return associated User Object"""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(80), nullable=False)
    theme = db.Column(db.String(10), default='dark')

    projects = db.relationship("Project", backref="user", lazy=True, cascade="all, delete, delete-orphan")

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def add_project(self, project_name):
        new_project = Project(name=project_name, user_id=self.id)
        db.session.add(new_project)
        db.session.commit()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    comments = db.Column(db.Text)
    archived = db.Column(db.Boolean(), nullable=False, default=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_update = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship("Item", backref="project", lazy=True, cascade="all, delete, delete-orphan")

    def archive_status(self, status):
        self.archived = status
        db.session.commit()

    def add_item(self, item_name):
        new_item = Item(project_id=self.id, name=item_name)
        db.session.add(new_item)
        db.session.commit()

    def get_completion(self):
        items = Item.query.filter_by(project_id=self.id).all()
        total_len = len(items)
        done_items = len([item for item in items if item.status == 'DONE'])
        if total_len and done_items:
            percent_completed = int((done_items / total_len) * 100)
            return percent_completed
        else:
            return 0

    def update_stamp(self):
        self.last_update = datetime.now()
        db.session.commit()

    def add_comment(self, comment):
        if not self.comments:
            self.comments = str(comment)
        else:
            formatted = " " + str(comment)
            self.comments += formatted
        db.session.commit()


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='TODO')

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def change_item_status(self, update):
        self.status = update

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()

