daemontools services
====================

This folder contains services controlled by the 
[daemontools](https://cr.yp.to/daemontools.html) 
([german documentation](https://wiki.uberspace.de/system:daemontools)).
Navigate into this folder and run ``svscan``. After this the json2mqtt-Service
is launched and it is connected to a logging service afterwards. Logs are placed in 
``json2mqtt/log/main``.