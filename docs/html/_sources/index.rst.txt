.. json2mqtt documentation master file, created by
   sphinx-quickstart on Tue Jul  4 14:07:20 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents:


Feinstaub Bridge
================


Data received as JSON via an HTTP POST request is send over to an MQTT
broker. A sample POST request originating from a
`luftdaten.info <http://luftdaten.info/>`_
sensor is of the following form.

.. code-block:: javascript

  POST / HTTP/1.1
  Host: 192.168.223.215
  Content-Type: application/json
  Authorization: Basic
  X-PIN: 0
  X-Sensor: esp8266-3394227
  Content-Length: 412
  Connection: close

  {"esp8266id": "3394227", "software_version": "NRZ-2017-090",
   "sensordatavalues":[{"value_type":"SDS_P1","value":"4.30"},
                       {"value_type":"SDS_P2","value":"3.53"},
                       {"value_type":"temperature","value":"20.80"},
                       {"value_type":"humidity","value":"52.30"},
                       {"value_type":"samples","value":"670215"},
                       {"value_type":"min_micro","value":"205"},
                       {"value_type":"max_micro","value":"505594"},
                       {"value_type":"signal","value":"-82"}]}


Installation
------------

Ansible can be used to install this tool as a service.

.. code-block:: bash

    $ ansible-playbook -K playbook-deploy.yml

Look into the `playbook-deploy.yaml-file
<https://github.com/tbs1-bo/feinstaub-json-mqtt-bridge/blob/master/playbook-deploy.yml>`_
to get more details about the deployment process.

The tool will be installed as daemontools service. Option ``-K`` asks for the
sudo-Passwort - only needed if daemontools must be installed.

To test the service you can now post a sample request found in the file
``sample_post.txt`` in the repo.

.. code-block:: bash

    curl -d @sample_post.txt -H 'Content-Type: application/json' localhost:8080/feinstaub/json2mqtt

daemontools services
--------------------

The folder ``services`` contains services controlled by the
`daemontools <https://cr.yp.to/daemontools.html>`_
(`german documentation <https://wiki.uberspace.de/system:daemontools>`_).
Navigate into this folder and run ``svscan``. After this the json2mqtt-Service
is launched and it is connected to a logging service afterwards. Logs are placed in
``json2mqtt/log/main``.

API-Doc
=======

The bottle-Server is configured and run in the following module.

json2mqtt
---------

.. automodule:: json2mqtt.run
   :members:

Links
=====

- Visit the project at `github
  <https://www.github.com/tbs1-bo/feinstaub-json-mqtt-bridge>`_.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
