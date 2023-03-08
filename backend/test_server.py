import requests

class TestServer:
    def test_get_testcase(self):
        r = requests.get("http://127.0.0.1:5000/get_testcase",params={"name":"tmp"})
        assert r.status_code ==200
