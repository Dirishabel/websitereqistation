import requests
class Catch():
    @classmethod
    def on_post(cls, req, resp):
        login = req.media.get("UserLogin")
        pwd = req.media.get("UserPassword")
        mail = req.media.get("UserMail")
        name = req.media.get("UserName")
        resp.body = json.dumps("hello "+name)
