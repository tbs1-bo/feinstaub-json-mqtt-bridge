import json2mqtt
import os


# activating virtual environment
activate_this = '/home/administrator/proj/feinstaub-json-mqtt-bridge-ve/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))


# change working directory
os.chdir(os.path.dirname(__file__))

json2mqtt.setup()

# fetch the application to be chosen for wsgi from the json2mqtt module
application = json2mqtt.application
