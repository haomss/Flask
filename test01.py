from flask import Flask, request,render_template, url_for
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


# @app.route("/")
# def hello_world1():
#     return 'Hello, World!'


# @app.route("/app", methods=['get', 'post'])  # 同下get()
# def hello_world2():
#     return 'Hello, app!'
#
#
# @app.route("/app/<tmp>", methods=['post'])  # 同下post()
# def hello_world3(tmp):
#     return f'Hello, {tmp}!'


# 命令行运行：curl -X POST -H "content-Type:application/json" -d "{'a':20}" 127.0.0.1:5000/app


class hello_world(Resource):

    def get(self):
        return 'hello app~~~~~'

    def post(self, tmp):
        return f"hello post------{tmp}"


class TestCase(Resource):
    def get(self):

        print(request.args)

        if "id" in request.args:
            print(app.config['testcase'])
            for i in app.config['testcase']:
                if i["id"] == int(request.args["id"]):
                    return i["id"]
        else:
            return app.config['testcase']

        return app.config['testcase']

    def post(self):

        if "id" not in request.json:
            return {"resutl": "errer", "errercode": 404}
        app.config['testcase'].append(request.json)
        return {"result": "ok", "errcode": "0"}
    # curl -X POST -d '{"a":20}' -H "content-Type:application/json" 127.0.0.1:5000/testcase


api.add_resource(hello_world, "/app/<tmp>")
api.add_resource(TestCase, "/run")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

