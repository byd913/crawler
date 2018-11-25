#encoding=utf-8

import flask
from flask import request
import logging
import os
import json
from logging.handlers import TimedRotatingFileHandler


app = flask.Flask(__name__)
VR_CODE_FILE = '/home/xiaoju/data/hospital/vr_code.txt'


@app.route('/hospital_vr_code')
def process_vr_code():
    ret_info = {'ret': 0, 'message': 'OK'}
    vr_code = request.args.get('vr_code', None)
    if not vr_code or not vr_code.isdigit():
        ret_info['ret'] = -1
        ret_info['message'] = 'vr code illegal'
        return json.dumps(ret_info)

    with open(VR_CODE_FILE, 'w') as fp:
        fp.write('%s' % (vr_code))
    return json.dumps(ret_info)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8032')