from flask import Flask
from  flask_sqlalchemy import SQLAlchemy

def test_sqlalchemy():
    app = Flask(__name__)
    with app.app_context():
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:hms131029@127.0.0.1:3306/testuser?charset=utf8mb4"# mysql -uroot -phms131029
        db = SQLAlchemy(app)



        class User(db.Model):
            id = db.Column(db.Integer,primary_key=True)
            username = db.Column(db.String(80),unique=True,nullable=False)
            email = db.Column(db.String(120),unique=False,nullable=False)

            def __repr__(self):
                return f'user:{self.username}'
        db.create_all()
        db.session.add(User(id=11,username="xiaoming1",email="123456@qq.com"))
        db.session.commit()


# if __name__ == '__main__':
#     test_sqlalchemy()