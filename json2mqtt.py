import paho.mqtt.client as mqtt
import bottle
import logging
import datetime

# TODO install as service

MQTT_HOST = "iot.eclipse.org"  # "localhost"
MQTT_TOPIC = "feinstaub/ebike/"
CLIENT = mqtt.Client()

@bottle.post("/feinstaub/json2mqtt")
def route_feinstaub_json2mqtt():
    # take the json and parse it
    json_req = bottle.request.json
    logging.debug("json req received %s", json_req)

    publish(json_req, MQTT_TOPIC)
    now = str(datetime.datetime.now())
    publish({"last_update": now}, MQTT_TOPIC)


def publish(json, topic_prefix):
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


@bottle.get("/feinstaub")
def route_index():
    # return page with current values
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    logging.debug("connecing to mqtt broker %s", MQTT_HOST)
    CLIENT.connect(MQTT_HOST)
    CLIENT.loop_start()

    bottle.run(host="0.0.0.0", port=8080, reloader=True)
