"""This module runs a bottle webserver and listens for a post request that
contains a JSON payload which will be transmitted over to an MQTT broker."""

import paho.mqtt.client as mqtt
import bottle
import logging
import datetime
import os

# TODO separate routes and logic

HTTP_PORT = 8080
MQTT_HOST = "localhost"
MQTT_TOPIC = "feinstaub/ebike/"
CLIENT = mqtt.Client()

application = bottle.default_app()


@application.post("/feinstaub/json2mqtt")
def route_feinstaub_json2mqtt():
    """The default route that is listening to post requests."""
    # take the json and parse it
    json_req = bottle.request.json
    logging.debug("json req received %s", json_req)

    publish(json_req, MQTT_TOPIC)
    now = str(datetime.datetime.now())
    publish({"stats/last_update": now,
             "stats/interval": 120}, MQTT_TOPIC)


def publish(json: dict, topic_prefix: str):
    """Take a JSON document and publish it to a given MQTT topic prefix."""
    for k in json:
        val = json[k]

        if type(val) is list:
            publish(dict(enumerate(val)), topic_prefix + str(k) + "/")
        elif type(val) is dict:
            publish(val, topic_prefix + str(k) + "/")
        else:
            t = topic_prefix + str(k)
            logging.debug("publishing to broker: '%s' '%s'", t, str(val))
            CLIENT.publish(topic=t, payload=val, retain=True)


@application.get("/feinstaub")
def route_index():
    # return page with current values
    pass


def setup():
    """Setup the MQTT-Client.

    If there is an HTTP_PORT environment variable, this will be used as
    value."""
    if "HTTP_PORT" in os.environ:
        global HTTP_PORT
        logging.debug("using http port from env var HTTP_PORT")
        HTTP_PORT = os.environ["HTTP_PORT"]

    logging.debug("connecting to mqtt broker %s", MQTT_HOST)
    CLIENT.connect(MQTT_HOST)
    CLIENT.loop_start()


def run_server():
    """Run the bottle-server on the configured http-port."""
    bottle.run(app=application,
               host="0.0.0.0", port=HTTP_PORT, reloader=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    setup()
    run_server()
