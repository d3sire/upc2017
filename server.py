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
from datetime import datetime, date
import numpy as np
import os
import argparse

from urllib.parse import quote

import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

companies_dbs = {}

PATH_TO_SCRIPT = '/home/www/'
if 'IS_DEV' in os.environ:
	PATH_TO_SCRIPT = '/Users/plentsov/google_drive/upc2017/'

# temporary client databases :)
companies_data = {
	28554: {
		'users': pd.read_csv(PATH_TO_SCRIPT + 'data/0_users.csv', parse_dates = ['registration_date']),
		'orders': pd.read_csv(PATH_TO_SCRIPT + 'data/0_orders.csv', parse_dates = ['date'])
	},
	28565: {
		'users': pd.read_csv(PATH_TO_SCRIPT + 'data/0_users.csv', parse_dates = ['registration_date']),
		'orders': pd.read_csv(PATH_TO_SCRIPT + 'data/0_orders.csv', parse_dates = ['date'])
	}
}

@app.route('/api/twist_incoming', methods = ['POST'])
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

	answer_start = """/oscar {}

**""".format(command_argument)

	is_plot = 0
	if 'plot' in text or 'dynamic' in text:
		is_plot = 1

	if command_argument.split()[0] == 'setup':
		answer = setup(workspace_id, command_argument.split()[1:])
	else:
		answer = query(command_argument, data['user_name'], workspace_id)

	answer['content'] = answer_start + answer['content'] + ('**' if is_plot == 0 else '')

	logging.warning(jsonify(answer).get_data(as_text=True))

	return jsonify(answer)


@app.route('/api/twist_configure', methods = ['GET'])
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

	return {'content': answer}


def query(text, user_name, workspace_id):
	"""
	Queries client's database
	"""
	dates_in_query = parse_dates(text)
	to_plot = 0
	start_date = None
	end_date = None

	if len(dates_in_query) > 0:
		start_date = dates_in_query[0]
		end_date = datetime.now().date() if len(dates_in_query) == 1 else dates_in_query[1]

	if 'plot' in text or 'dynamic' in text:
		to_plot = 1

	question_target = 'not_understood'
	if 'user' in text and to_plot == 0: 
		question_target = 'n_users_static' 
	elif 'user' in text and to_plot == 1:
		question_target = 'n_users_dynamic'
	elif 'order' in text and to_plot == 0:
		question_target = 'n_orders_static'
	elif 'order' in text and to_plot == 1:
		question_target = 'n_orders_dynamic'

	# aggregating data
	data = None

	if question_target in 'n_users_static':
		data = companies_data[workspace_id]['users'].copy()
		if start_date:
			data = data.loc[data.registration_date >= start_date].copy()
			data = data.loc[data.registration_date <= end_date].copy()
			data = 'Total number of users between {} and {} is {}'.format(start_date, end_date, len(data))
		else:
			data = 'Total number of users is {}'.format(len(data))

	elif question_target in 'n_orders_static':
		data = companies_data[workspace_id]['orders'].copy()
		if start_date:
			data = data.loc[data.date >= start_date].copy()
			data = data.loc[data.date <= end_date].copy()
			data = 'Total number of orders between {} and {} is {}'.format(start_date, end_date, len(data))
		else:
			data = 'Total number of orders is {}'.format(len(data))

	elif question_target in 'n_users_dynamic':
		data = companies_data[workspace_id]['users'].copy()
		if start_date:
			data = data.loc[data.registration_date >= start_date].copy()
			data = data.loc[data.registration_date <= end_date].copy()
		else:
			start_date = data.registration_date.min()
			end_date = data.registration_date.max()

		content = 'Dynamics of number of users between {} and {}:**\n\n'.format(start_date, end_date)
		
		fig, ax = plt.subplots()

		plot_gr = plot_granularity(start_date, end_date)
		if plot_gr == 'day':
			data.groupby('registration_date').size().plot(ax = ax)
		elif plot_gr == 'week':
			data['registration_week'] = data['registration_date'].dt.strftime('%Y-%U')
			data.groupby('registration_week').size().plot(kind = 'bar', ax = ax)
		elif plot_gr == 'month':
			data['registration_month'] = data['registration_date'].dt.strftime('%Y-%m')
			data.groupby('registration_month').size().plot(ax = ax)

		filename = 'plot_' + str(datetime.now()) + '.png'
		plt.title('Number of registrations')
		fig.savefig(PATH_TO_SCRIPT + 'plots/' + filename)

		data = {'content': content + 'https://plentsov.com/static/' + quote(filename)}

	elif question_target in 'n_orders_dynamic':
		data = companies_data[workspace_id]['orders'].copy()
		if start_date:
			data = data.loc[data.date >= start_date].copy()
			data = data.loc[data.date <= end_date].copy()
		else:
			start_date = data.date.min()
			end_date = data.date.max()

		content = 'Dynamics of number of orders between {} and {}:**\n\n'.format(start_date, end_date)
		
		fig, ax = plt.subplots()

		plot_gr = plot_granularity(start_date, end_date)
		if plot_gr == 'day':
			data.groupby('date').size().plot(ax = ax)
		elif plot_gr == 'week':
			data['week'] = data['date'].dt.strftime('%Y-%U')
			data.groupby('week').size().plot(kind = 'bar', ax = ax)
		elif plot_gr == 'month':
			data['month'] = data['date'].dt.strftime('%Y-%m', ax = ax)
			data.groupby('month').size().plot()

		filename = 'plot_' + str(datetime.now()) + '.png'
		plt.title('Number of orders')
		fig.savefig(PATH_TO_SCRIPT + 'plots/' + filename)

		data = {'content': content + 'https://plentsov.com/static/' + quote(filename)}

	else:
		data = 'No entiendo, ' + str(user_name)

	return {'content': data}


def plot_granularity(start_date, end_date):
	"""
	Returns type of time periods to use for plotting
	"""
	datediff = end_date - start_date
	datediff = datediff.days

	if datediff <= 30:
		return 'day'
	if datediff <= 90:
		return 'week'
	return 'month'


def parse_dates(query):
    """
    Extract max 2 dates from query text, including like 'september 1st', 'yesterday'
    """

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

if __name__ == '__main__':
	app.run()