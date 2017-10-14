from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
import pandas as pd
from dateparser import parse

app = Flask(__name__)

companies_dbs = {}

companies_data = {
	1488: {
		'users': 1888
	}
}

@app.route('/twist_incoming', methods = ['POST'])
def incoming():
	"""
	Hook for the twist
	"""
	data = request.get_json(silent = True)
	event_type = data['event_type']
	if event_type == 'ping':
		return jsonify({'content': 'pong'})
	command = data['command']
	command_argument = data['command_argument']
	return jsonify([command, command_argument])



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


def parse_dates(query):

    words = query.split()

    words_parsed = [0] * len(words)
    for i in range(len(words)):
        for j in range(i, len(words)):
            candidate = ' '.join(words[i:j+1])
            if parse(candidate):
                words_parsed[i:j+1] = [1]*(j+1-i)

    for i in range(len(words)):
        if words[i] in ['and', 'to']:
            words_parsed[i] = 0
                
    parsed_dates = []
    current_date = ''
    for i in range(len(words)+1):
        if i == len(words) or words_parsed[i] == 0:
            if current_date:
                parsed_dates.append(parse(current_date).date())
            current_date = ''
        else:
            current_date = current_date + (' ' if current_date else '')  + words[i]

    parsed_dates = sorted(parsed_dates)
    dates_to_return = []
    if len(parsed_dates) > 0:
        dates_to_return.append(parsed_dates[0])
    if len(parsed_dates) > 1:
        dates_to_return.append(parsed_dates[len(parsed_dates) - 1])
    
    return parsed_dates

app.run()