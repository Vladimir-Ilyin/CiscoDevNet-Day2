#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask_cors import CORS
from flask import request

from app_find_mac import gather_info, find_mac

app = Flask(__name__)
CORS(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')

@app.route('/getmac/api/v1.0/macs', methods=['GET'])
def get_macs():
    # API возвращает список всех MAC адресов в формате ['SwitchName','Port','Mode','Vlan','MAC']
    full_table = gather_info()
    data = []
    for row in full_table:
        data.append(dict(zip(['SwitchName','Port','Mode','Vlan','MAC'], [row['host'],row['destination_port'],row.get('mode', 'UNDEFINED'),row['vlan'],row['destination_address']])))
    return jsonify({'data': data})

@app.route('/getmac/api/v1.0/mac/<string:mac>', methods=['GET'])
def get_mac(mac):
    # API возвращает найденный MAC адрес в формате ['SwitchName','Port','Mode','Vlan','MAC']
    # если MAC не найде, возвращает 404

    mode = request.args.get('mode', default = '', type = str)
    full_table = gather_info()

    result = find_mac(full_table,mac,mode)

    if len(result) == 0:
        abort(404)
    else:
        data = []
        for row in result:
            data.append(dict(zip(['SwitchName','Port','Mode','Vlan','MAC'], [row['host'],row['destination_port'],row.get('mode', 'UNDEFINED'),row['vlan'],row['destination_address']])))
        return jsonify({'data': data})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000',debug=True)
