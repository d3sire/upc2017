from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
import pandas as pd
from dateparser import parse
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from datetime import datetime

app = Flask(__name__)

companies_dbs = {}


# temporary client databases :)
companies_data = {
	28554: {
		'users': 1888
	},
	28565: {
		'users': 2135
	}
}

@app.route('/twist_incoming', methods = ['POST'])
def incoming():
	"""
	Hook for the twist
	"""
	data = request.form
	#print(request.form)

	# incorrect data
	if not data:
		return jsonify('Something gone wrong')

	# if pinging
	event_type = data['event_type']
	if event_type == 'ping':
		return jsonify({'content': 'pong'})


	command = data['command'] # should be oscar
	command_argument = data['command_argument']
	workspace_id = int(data['workspace_id'])

	answer = """/oscar ' + command_argument

	"""

	if command_argument.split()[0] == 'setup':
		answer += setup(workspace_id, command_argument.split()[1:])
	elif len(command_argument.split()) > 1 and command_argument.split()[0] == 'plot':
		answer += query_plot(' '.join(command_argument.split()[1:]))
	else:
		answer += query(command_argument, data['user_name'], workspace_id)

	return jsonify({'content': answer})


@app.route('/twist_configure', methods = ['GET'])
def configure():
	"""
	Called when integration has been installed
	"""
	return jsonify('configured')


def setup(workspace_id, args):
	"""
	Initiates connection to client's database
	"""

	if len(args) != 3:
		answer = 'Please use setup this way: "\oscar setup dbtype host ssh_key"'
	else:
		dbtype = args[0]
		server = args[1] 
		key = args[2]

		companies_dbs[workspace_id] = {
			'server': server,
			'key': key,
			'dbtype': dbtype
		}

		answer = 'Connection to {} was successfully installed'.format(dbtype)

	return answer


def query(text, user_name, workspace_id):
	"""
	Queries client's database
	"""
	if 'user' in text:
		answer = 'There are ' + str(companies_data[workspace_id]['users']) + ' users.'
	else:
		answer = 'No entiendo, ' + str(user_name)

	return answer


def query_plot(text):
	"""
	Returns a plot from query
	"""
	data = json.loads(query(text))['content']
	plt.plot(data)
	filename = 'plot_' + str(datetime.now())
	plt.savefig('plots/' + filename)

	answer = {
		'content': 'Here is your plot',
		'attachments': [
			{
				'file_type': 'image/png',
				'file_name': filename,
				'url': '',
				'attachment_id': '',
				'upload_state': ''
			}
		]
	}

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