===============
Troubleshooting
===============

If you have issues with the ``esp8266`` not connecting on /dev/ttyUSB, but the device does show up in lsusb:

.. code:: console

    $ lsusb
    [..]
    Bus 001 Device 019: ID 1a86:7523 QinHeng Electronics CH340 serial converter
    [..]

Then this might be related to a udev rule in Linux. 
Removing this rule will stop udev from hijacking the USB device.

.. code:: console

    sudo rm /usr/lib/udev/rules.d/*-brltty-*.rules
    sudo udevadm control --reload-rules
    sudo systemctl mask brltty.path 

ESPlorer
========
``ESPlorer`` is a tool that allows you to flash firmware to the ESP8266 using a GUI. This is example code on how to build and run it:

.. code-block:: consoleabap

    git clone https://github.com/4refr0nt/ESPlorer.git

    # Build it
    ./mvnw clean package

    # Run it
    java -jar target/ESPlorer.jar

The ``ESPlorer`` can be used to interact with the ``esp8266`` and flash binaries using a GUI.