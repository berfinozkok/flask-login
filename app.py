from flask import Flask, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user #does not care how data stored, uses dictionary,
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///user1.db' #
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
login=LoginManager(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model): #to import tables to database - from app import db
    id=db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(20))
    #after creating class variables db.create_all()

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

admin=Admin(app, index_view=MyAdminIndexView())
admin.add_view(ModelView(User, db.session))

@app.route('/login')
def login():
    user=User.query.get(1)
    login_user(user)
    return 'Logged in!'

@app.route('/logout')
def logout():
    logout_user()
    return 'Logged out!'

if __name__=='__main__':
    app.run(debug=True)