from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
import pandas as pd

app = Flask(__name__)

companies_dbs = {}

companies_data = {
	1488: {
		'users': 1888
	}
}



@app.route('/setup')
def setup():
	"""
	Creates company_id and stores db credentials for this company
	"""
	company_id = 1488
	server = request.args.get('server', '')
	key = request.args.get('key', '')
	dbtype = request.args.get('dbtype', '')

	companies_dbs[company_id] = {
		'server': server,
		'key': key,
		'dbtype': dbtype
	}

	return jsonify(company_id)


@app.route('/query')
def query():
	"""
	Queries db
	"""
	company_id = 1488
	text = request.args.get('text', '')
	q_type = request.args.get('type', '')

	answer = ''
	if q_type == 'users':
		answer = 'There are ' + str(companies_data[company_id]['users']) + ' users'

	return jsonify(answer)




app.run()