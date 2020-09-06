from datetime import datetime

import falcon
from falcon.http_status import HTTPStatus
from loguru import logger

from config import LOGFILE
from app_code.catch_web_resourse import Catch

class LogWrite():
    """ логирование результатов отработки API """
    @classmethod
    def process_request(cls, req, _):
        """ записываем время начала отработки """
        req.context["start_time"] = datetime.now()

    @classmethod
    def process_response(cls, req, resp, resource, req_succeeded):
        # pylint: disable=unused-argument
        """ записываем в лог файл """
        now = datetime.now()
        delta = now - req.context["start_time"]
        time_ = int(delta.total_seconds() * 1000)
        token = req.get_header('Authorization')
        if resp.status[:3] == '200':
            logger.info("{} {} | {} | {} ms | {}"
                        .format(req.method, req.path, resp.status, time_,
                                req.content_length))
        else:
            logger.error("{} {} | {} | {} ms\n token='{}'\n {}"
                         .format(req.method, req.path, resp.status, time_,
                                 token, req.media))
class HandleCORS(object):
    """ set CORS headers """

    def process_request(self, req, resp):
        """ set header """
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header("Access-Control-Allow-Methods", "*")
        resp.set_header('Access-Control-Allow-Headers', "*")
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_200, body='\n')


logger.add(LOGFILE, rotation="50 MB")
APP = falcon.API(middleware=[LogWrite(), HandleCORS()])
catch = Catch()
APP.add_route('/send',catch)
