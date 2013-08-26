ARDUINO/RASPBERRY PI GARDEN
---------------------------
![alt tag](https://raw.github.com/sangallimarco/arduino_raspberry_garden_ui/master/static/img/screenshot_status.png)

Requirements
------------
pip install -r requirements.txt

Configuration
-------------
copy the main.cfg.template to main.cfg and choose the right engine

Let's Start
-----------
python main.py

now open a browser and go to address http://localhost:8080

Raspberry pi InitScript
-----------------------
Open a shell and execute:

* cp scripts/garden in /etc/init.d
* chmod +x /etc/init.d/garden
* update-rc.d garden defaults
* reboot


