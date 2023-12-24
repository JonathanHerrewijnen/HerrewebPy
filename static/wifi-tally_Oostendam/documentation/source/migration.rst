=====================
Migrating to a new PC
=====================
When migrating to a new computer, you need to do the following:

    1. Configure the new computer to use the *same* IP address as the previous computer.
    2. Install `NodeJS and NPM <https://nodejs.org/en/download>`_
    3. Copy the config.json from the old PC (homedir + .wifi-tally.json) to the same location on the new PC.
    4. Run the server on the host PC(see below)

Run server
==========
To run the server, navigate to ``wifi-tally/hub`` and execute ``run_server.sh``

.. code-block:: console

    $ ./run_server.sh 

    > wifi-tally-hub@0.1.0 start
    > node server.js --env=production

    Using mixer configuration "null"
    No video mixer connected.
    Listening for Tallies on 0.0.0.0:7411
    Web Server available on http://localhost:3000
    (node:117081) ExperimentalWarning: The Fetch API is an experimental feature. This feature could change at any time