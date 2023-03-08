import os
from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, abort
from jenkinsapi.jenkins import Jenkins

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:hms131029@127.0.0.1:3306/testuser?charset=utf8mb4"  # mysql -uroot -phms131029
db = SQLAlchemy(app)
api = Api(app)
app.config['testcase'] = []


class TestCase(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    description = db.Column(db.String(80), unique=False, nullable=True)
    filename = db.Column(db.String(80), unique=False, nullable=False)
    content = db.Column(db.String(300), unique=False, nullable=False)
    report = db.relationship("Report", backref="test_case", lazy=True)

    def __repr__(self):
        return f'user:{self.name}'


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), unique=False, nullable=True)
    dir = db.Column(db.String(300), unique=False, nullable=False)
    testcase_id = db.Column(db.String(80), db.ForeignKey("test_case.name"), nullable=False)

    def __repr__(self):
        return f'user:{self.name}'


class TestCaseServer(Resource):

    def post(self):
        """
        用例存储，将用例文件放入数据库中
        :return:
        """
        if "file" in request.files and "name" in request.form:
            f = request.files["file"]
            name = request.form[
                "name"]  # 接收name。curl -F "file=@tmp.py" -F "name=aaa" http://127.0.0.1:5000/testcase;传一个name
            file_name = f.filename
            content = f.read()
            testcase = TestCase(name=name, filename=file_name, content=content)
            db.session.add(testcase)
            db.session.commit()
            f.save(os.path.join("./", file_name))  # 保存到本地
            return "ok"
            # curl -F "file=@tmp.py" http://127.0.0.1:5000/testcase

        abort(404)  # 返回不同状态码，和默认的错误页


# class TestCaseRun(Resource):
#     def get(self):
#         """
#         用例存储
#         :return:
#         将用例从数据库取出来存到本地abc.py中：curl -o "abc.py" http://127.0.0.1:5000/run
#         """
#         testcase = TestCase.query.filter_by(name="tmp").first()
#
#         return testcase.content  # flask_restful插件会将结果转为字符串格式："def test_a():\n    print(\"11111\")\ndef test_b():\n    print(\"22222\")\n"；所以先用原生的flask，如下：


@app.route("/get_testcase", methods=["get"])
def run_testcase():
    """
    用例存储,将用例从数据库取出来存到本地abc.py中：curl -o "abc.py" http://127.0.0.1:5000/run
    :return:
    """
    if "name" in request.args:
        name = request.args["name"]
        testcase = TestCase.query.filter_by(name=name).first()
        print(testcase)
        return testcase.content
    abort(404)


@app.route("/run", methods=["get"])
def run():
    """
    调Jenkins，执行拉取用例
    :return:
    """
    if "name" in request.args:
        name = request.args["name"]
        testcase = TestCase.query.filter_by(name=name).first()

        J = Jenkins("http://127.0.0.1:8080/", username="jenkins_hms", password="119310860ad950bacb16c9f1a667a7ab8c")
        print(J.keys())
        J["tmp_flask"].invoke(build_params={"name": name, "filename": testcase.filename})  # 运行Jenkins
        return "ok"


@app.route("/report_upload", methods=["post"])
def report_upload():
    if "file" in request.files and "name" in request.form:
        f = request.files["file"]
        name = request.form[
            "name"]  # 接收name。curl -F "file=@tmp.py" -F "name=aaa" http://127.0.0.1:5000/testcase;传一个name
        file_name = f.filename
        DIR = "/Users/haomengshan/haomst1/tmp_flask"
        dir = os.path.join(DIR,file_name)
        report = Report(dir=dir, testcase_id=name)
        db.session.add(report)
        db.session.commit()
        f.save(os.path.join("./", file_name))  # 保存到本地
        return "ok"
        # curl -F "file=@tmp.py" http://127.0.0.1:5000/testcase

    abort(404)  # 返回不同状态码，和默认的错误页


api.add_resource(TestCaseServer, "/testcase")
# api.add_resource(TestCaseRun, "/run")

if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
