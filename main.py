from flask import Flask, request, session, render_template, flash, redirect, url_for, jsonify
from gardenController import *
from testThread import *

#####################################################
app = Flask(__name__)

#threaded process
garden = customEngine("192.168.1.177")
gardenBridge = gardenBridge()

#######################
# home page ###########
#######################
@app.route('/', methods=['GET', 'POST'])
def index():
	name = request.args.get('name', '')
	if name != '':
		flash('Single Pump On', 'error')
		return redirect(url_for('index'))
	else:
		return render_template('index.html',name="index")

	return render_template('index.html',name=name)

#######################
# call it from cron ###
#######################
@app.route('/activate')
def activate():
	#get values from testThread
	temp,humidity,wind,rain,switch = gardenBridge.getForecast()
	delay = gardenBridge.getDelay()

	#if condition satisfied put engine on!
	connected = garden.isConnected() 
	if switch and connected:
		if rain<1:
			garden.pumpsOn(delay)
		else:
			garden.singlepumpOn(delay)

	#return a flag
	return jsonify(connected=connected, switch=switch)
	
#######################
# render status #######
#######################
@app.route('/status', methods=['GET', 'POST'])
def status():
	#get parameters
	if request.method == 'POST':
		gardenBridge.setParams(request.form['temp'], request.form['humidity'], request.form['wind']) 
		flash('New params saved', 'success')
		return redirect(url_for('status'))

	#get params back
	temp,humidity,wind,rain,switch = gardenBridge.getForecast()
	delay = gardenBridge.getDelay()
	
	#render page
	flash('Pumps On!', 'Welcome')
	return render_template('status.html',name="index")

#######################
# 404 error ###########
#######################
@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'),404

#####################################################
if __name__ == '__main__':
	#run server
	app.debug = True
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run(host='0.0.0.0',port=8080,threaded=True)

	