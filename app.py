from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_marshmallow import Marshmallow
from flask_restx import Api, Resource
# from serializers import UserSerializer, PostSerializer
# from models import User, Post

db = SQLAlchemy()
ma = Marshmallow()

app = Flask(__name__)

#Инициализация базы в Alchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_db.db"
#Тема
app.config["FLASK_ADMIN_SWATCH"] = "cyborg"

app.config["SECRET_KEY"] = "qwertyuiop"

admin = Admin(app, name='flask_app', template_mode='bootstrap4')

#Инициализация Alchemy и Marshmallow в приложении
db.init_app(app)
ma.init_app(app)

api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean, default=False)

class UserSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class PostSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post

#Создание базы данных
with app.app_context():
    db.create_all()

@app.route('/home')
def hello_world():
    return render_template('hello_world.html')

@api.route('/user_list/', endpoint='user_list')
class UserList(Resource):
    def get(self):
        list_shema = UserSerializer(many=True)
        return list_shema.dump(User.query.all()), 200

@api.route('/post_list/', endpoint='post_list')
class PostList(Resource):
    def get(self):
        list_shema = PostSerializer(many=True)
        return list_shema.dump(Post.query.all()), 200


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))

if __name__ == "__main__":
    app.run(debug=False)