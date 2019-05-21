# coding=utf-8
from apis import api
from database import create_app
import logging

__author__ = 'Yuxia'

logging.basicConfig(level=logging.INFO,
                    filename='./log-file.txt',
                    filemode='w',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


if __name__ == '__main__':

    logging.info('main module start')

    app = create_app('config.py')
    api.init_app(app)
    app.run(port=8080, debug=True)
    # # Production
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()
    logging.info('main module stop')