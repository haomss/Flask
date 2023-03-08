from jenkinsapi.jenkins import Jenkins


def test_jenkins():
    J = Jenkins("http://127.0.0.1:8080/", username="jenkins_hms", password="119310860ad950bacb16c9f1a667a7ab8c")
    print(J.keys())
    J["tmp_flask"].invoke(build_params={"name":"tmp","filename":"tmp.py"})#运行Jenkins
