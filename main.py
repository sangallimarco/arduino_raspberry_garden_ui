#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, session, render_template, flash, redirect, url_for, jsonify
import ConfigParser
import importlib
import sys
from forecasts.openweathermap import customBridge

reload(sys)
sys.setdefaultencoding('utf-8')

#####################################################
# load configuration ################################
#####################################################
cf ='%s/main.cfg' % sys.path[0]
config = ConfigParser.ConfigParser()
config.read(cf)

#####################################################
# init threads ######################################
#####################################################
app = Flask(__name__)

#threaded process
path = 'engines.%s' % config.get('engine','type')
ip = config.get('engine','ip')
pins = config.get('engine','pins').split(',')

#
try:
	customEngine = getattr(importlib.import_module(path),'customEngine')
except:
	path = 'engines.dummy'
	customEngine = getattr(importlib.import_module(path),'customEngine')


#set engine
garden = customEngine(ip, pins)

#bridge
# path = 'forecasts.%s' % config.get('forecast','type')
# try:
# 	customBridge = getattr(importlib.import_module(path),'customBridge')
# except:
# 	path = 'forecasts.uk'
# 	customBridge = getattr(importlib.import_module(path),'customBridge')

gardenBridge = customBridge(config.get('forecast','key'))

#####################################################
# Flask controllers #################################
#####################################################

#######################
# filter booleans #####
#######################
@app.template_filter('bool_filter')
def bool_filter(s):
    if type(s) == bool:
    	if s:
    		return '<i class="icon icon-ok"></i>'
    	else:
    		return '<i class="icon icon-remove"></i>'
    else:
    	return s

#######################
# home page ###########
#######################
@app.route('/')
def index():
	return render_template('index.html')

#######################
# ajax calls ##########
#######################
@app.route('/activate/<type>')
def activate(type):
	#get values from testThread
	switch,params = gardenBridge.getForecast()
	hparams = gardenBridge.getParams()
	message = 'All Pumps Off'
	message_type = 'success'

	#check ts
	if type == 'test':
		delay = 10
	else:
		delay = hparams['delay']

	#if condition satisfied put engine on!
	connected = garden.isConnected()
	if connected:
		if garden.isReady():
			if switch and not params['rain']:
				garden.pumpsOn(delay)
				message = 'All Pumps On'
			else:
				garden.singlepumpOn(delay)
				message = 'Single Pump On'
		else:
			message = 'System is Running'
			message_type = 'error'

	#return a flag
	return jsonify(connected=connected, switch=switch, rain=params['rain'], message=message, message_type=message_type)

@app.route('/stop')
def stop():
	garden.stop()
	message_type = 'error'
	message = 'All Pumps Off'
	return jsonify(status = True , message=message, message_type=message_type)

@app.route('/refresh')
def refresh():
	#get status pumps
	switch,params = gardenBridge.getForecast()
	status = garden.isReady()
	connection = garden.isConnected()
	#
	return jsonify(connection = connection,status = status, params = params, switch = switch)

#######################
# call it from cron ###
#######################
@app.route('/check')
def check():
	#get values from testThread
	switch,params = gardenBridge.getForecast()
	if params['current']:
		params['forecast'] = True
	else:
		params['forecast'] = False

	hparams = gardenBridge.getParams()

	#if condition satisfied put engine on!
	connected = garden.isConnected()

	#check if pumps are not working
	ready = garden.isReady()

	#return
	return render_template('check.html',params=params,hparams=hparams,connected=connected,ready=ready)

#######################
# render status #######
#######################
@app.route('/status', methods=['GET', 'POST'])
def status():
	#get parameters
	if request.method == 'POST':
		gardenBridge.setParams(request.form['temp'], request.form['humidity'], request.form['wind'],request.form['delay'],request.form['postcode'])
		flash('New params saved', 'success')
		return redirect(url_for('status'))

	#get params back
	switch,params = gardenBridge.getForecast()
	hparams = gardenBridge.getParams()

	#check if pumps are not working
	ready = garden.isReady()

	#render page
	return render_template('status.html',switch=switch,params=params,hparams=hparams,ready=ready)

#######################
# 404 error ###########
#######################
@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'),404

#####################################################
# main loop #########################################
#####################################################
if __name__ == '__main__':
	#run server
	app.debug = config.getboolean('server', 'debug')
	app.secret_key = config.get('server', 'secret')
	app.run(host='0.0.0.0',port=8080,threaded=True)
