from flask import Flask, request, session, render_template, flash, redirect, url_for, jsonify
import ConfigParser, sys
from gardenController import *

#####################################################
cf ='%s/main.cfg' % sys.path[0]
config = ConfigParser.ConfigParser()
config.read(cf)

#####################################################
app = Flask(__name__)

#threaded process
garden = customEngine(config.get('arduino', 'ip'))
gardenBridge = gardenBridge()

#######################
# home page ###########
#######################
@app.route('/')
def index():
	return render_template('index.html')

#######################
# call it from cron ###
#######################
@app.route('/activate')
def activate():
	#get values from testThread
	switch,params = gardenBridge.getForecast()
	hparams = gardenBridge.getParams()
	pumps = 'Off'

	#if condition satisfied put engine on!
	connected = garden.isConnected() 
	if switch and connected:
		if garden.isReady():
			if not params['rain']:
				garden.pumpsOn(hparams['delay'])
				pumps = 'All'
			else:
				garden.singlepumpOn(hparams['delay'])
				pumps = 'Single'
		else:
			pumps = 'Running'

	#return a flag
	return jsonify(connected=connected, switch=switch, rain=params['rain'], pumps=pumps)
	
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

	#return
	return render_template('check.html',params=params,hparams=hparams,connected=connected)

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

	#render page
	return render_template('status.html',switch=switch,params=params,hparams=hparams)

#######################
# force system ########
#######################
@app.route('/remote/<type>')
def remote(type):
	#if condition satisfied put engine on!
	connected = garden.isConnected()
	hparams = gardenBridge.getParams()
	if connected: 
		#check if is ready to accept a new queue
		if garden.isReady():
			if type == 'all':
				garden.pumpsOn(hparams['delay'])
				flash('All Pumps Activated', 'success')
			else:
				garden.singlepumpOn(hparams['delay'])
				flash('Protected Area Pump Activated', 'success')
		else:
			flash('Pumps Running...', 'warning')
	else:
		flash('ARDUINO not connected!', 'error')

	#return a flag
	return redirect(url_for('status'))

#######################
# 404 error ###########
#######################
@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'),404

#####################################################
if __name__ == '__main__':
	#run server
	app.debug = config.get('server', 'debug'),
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run(host='0.0.0.0',port=8080,threaded=True)

	