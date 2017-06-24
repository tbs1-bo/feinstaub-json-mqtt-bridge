Feinstaub Bridge
================

Receive data via post request and send them to an MQTT broker. A Post
request is of the following form.

````
POST / HTTP/1.1
Host: 192.168.223.215
Content-Type: application/json
Authorization: Basic
X-PIN: 0
X-Sensor: esp8266-3394227
Content-Length: 412
Connection: close

{"esp8266id": "3394227", "software_version": "NRZ-2017-090", "sensordatavalues":[{"value_type":"SDS_P1","value":"4.30"},{"value_type":"SDS_P2","value":"3.53"},{"value_type":"temperature","value":"20.80"},{"value_type":"humidity","value":"52.30"},{"value_type":"samples","value":"670215"},{"value_type":"min_micro","value":"205"},{"value_type":"max_micro","value":"505594"},{"value_type":"signal","value":"-82"}]}
````

Installation
------------

    pip install -r requirements.txt

To test the service you can post a sample request from the repo.

    curl -d @sample_post.txt -H 'Content-Type: application/json' localhost:8080/feinstaub/json2mqtt
