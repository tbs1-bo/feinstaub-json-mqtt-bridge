import paho.mqtt.client as mqtt
import bottle
import logging

# TODO install as service

MQTT_HOST = "localhost"
MQTT_TOPIC = "/feinstaub/"

"""
sample post follows

POST / HTTP/1.1
Host: 192.168.223.215
Content-Type: application/json
Authorization: Basic
X-PIN: 0
X-Sensor: esp8266-3394227
Content-Length: 412
Connection: close

{"esp8266id": "3394227", "software_version": "NRZ-2017-090", "sensordatavalues":[{"value_type":"SDS_P1","value":"4.30"},{"value_type":"SDS_P2","value":"3.53"},{"value_type":"temperature","value":"20.80"},{"value_type":"humidity","value":"52.30"},{"value_type":"samples","value":"670215"},{"value_type":"min_micro","value":"205"},{"value_type":"max_micro","value":"505594"},{"value_type":"signal","value":"-82"}]}
"""

@bottle.post("/feinstaub/json2mqtt")
def route_feinstaub_json2mqtt():
    # take the json and parse it
    json_req = bottle.request.json
    logging.debug("json req received %s", json_req)

    # send json data to mqtt
    client = mqtt.Client()
    client.connect(MQTT_HOST)  # connecting with default port 1883

    publish(json_req, client, MQTT_TOPIC)
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
            logging.debug("publishing to broker: %s %s", t, val)
            client.publish(topic=t, payload=val, retain=True)
    

@bottle.get("/feinstaub")
def route_index():
    # return page with current values
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    bottle.run(host="0.0.0.0", port=8080, reloader=True)

