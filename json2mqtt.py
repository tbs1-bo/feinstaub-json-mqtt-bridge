import paho.mqtt.client as mqtt
import bottle
import logging
import time

# TODO install as service

MQTT_HOST = "localhost"
MQTT_TOPIC = "feinstaub/ebike/"


@bottle.post("/feinstaub/json2mqtt")
def route_feinstaub_json2mqtt():
    # take the json and parse it
    json_req = bottle.request.json
    logging.debug("json req received %s", json_req)

    # send json data to mqtt
    client = mqtt.Client()    
    client.loop_start()
    client.connect(MQTT_HOST)  # connecting with default port 1883

    publish(json_req, client, MQTT_TOPIC)
    publish({"last_update":time.time()}, client, MQTT_TOPIC)
    # client.publish(MQTT_TOPIC+"last_update", payload=time.time(), retain=True)
    client.loop_stop()
    client.disconnect()


def publish(json, client, topic_prefix):
    for k in json:
        val = json[k]

        if type(val) is list:
            publish(dict(enumerate(val)), client, topic_prefix + str(k) + "/")
        elif type(val) is dict:
            publish(val, client, topic_prefix + str(k) + "/")
        else:
            t = topic_prefix + str(k)
            logging.debug("publishing to broker: '%s' '%s'", t, val)
            client.publish(topic=t, payload=val, retain=True)
    

@bottle.get("/feinstaub")
def route_index():
    # return page with current values
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    bottle.run(host="0.0.0.0", port=8080, reloader=True)

