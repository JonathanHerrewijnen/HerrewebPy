================
Tallies Overview
================

This page gives a short overview of how the tallies work in relation to the camera's. A simple overview of the tallies in correlation between the server and the streamer is shown below:

.. drawio-image:: overview.drawio



Hardware
========

The hardware for the tallies is an ``esp8266`` microcontroller, as they can be found `on Amazon <https://www.amazon.nl/Diymore-ESP8266-WiFi-ontwikkelingskaart-NodeMCU-ESP-12E-module/dp/B09Z6T2XS4/ref=sr_1_2_sspa?__mk_nl_NL=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3DHTKU7SQKET9&keywords=esp8266&qid=1674509572&sprefix=esp8266%2Caps%2C135&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1>`_. 
These microcontrollers are very cheap but are capable of using the ``802.11 b/g/n`` wifi standard(``IEEE``).

A quick overview of the hardware:


+-------------------------+--------------------------------------+
| Type                    | Value                                |
+=========================+======================================+
| CPU                     | 32Bit RISC based on ``Xtensa lx106`` |
+-------------------------+--------------------------------------+
| Instruction RAM         | 32 KiB                               |
+-------------------------+--------------------------------------+
| Instruction Cache       | 32 KiB                               |
+-------------------------+--------------------------------------+
| User Data RAM           | 80 KiB                               |
+-------------------------+--------------------------------------+
| System Data RAM         | 16 KiB                               |
+-------------------------+--------------------------------------+
| Flash Memory (External) | 4 MiB                                |
+-------------------------+--------------------------------------+

Of the 17 GPIO pins available, only 3 are used for the RGB colouring. 
Wifi is used for communication between the tallies and a server that will tell the tally to turn on the lights.

Software
========
On the Host a ``NodeJS`` server is run that opens a websocket on port ``7411``. 
This websockets waits for tallies to connect and sends data to them when connected.
The server also connects to the streamer, in our case a ``Black Magic ATEM`` that controls the camera's. 
The streamer gives information about which camera is active which is passed to the tallies.



