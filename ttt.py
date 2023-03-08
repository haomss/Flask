from flask import Flask

app = Flask(__name__)  # 在当前文件下创建应用


@app.route("/")  # 装饰器，url，路由
def index():  # 试图函数

    return "hello world"

if __name__ == '__main__':
    app.run()




