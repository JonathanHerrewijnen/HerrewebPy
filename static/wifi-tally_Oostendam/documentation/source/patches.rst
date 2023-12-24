=============
Tally Patches
=============
This section describes the patches made to the software. These patches are provided in the repository so no user interaction is needed when building the firmware.

LED patches
===========
The goal of the patches is to:

    * Disable any signal leds on error, like no wifi connected or server not accessble
    * Disable green led when on preview

In order to add these patches the following code was edited in the firmware:

.. code-block:: c

    _G.MyLed = {
        signal that nothing is being done
        initial = flashPattern("O", colors.BLUE),
        waitForWifiConnection = flashPattern("Oo", colors.GREEN),
        invalidSettingsFile = flashPattern("OoOoOooooooo", colors.BLUE, 2),
        waitForWifiIp = flashPattern("OoOo", colors.BLUE),
        waitForServerConnection = flashPattern("OoOooo", colors.BLUE),
        onPreview = flashPattern("O", colors.GREEN),
        onAir = flashPattern("O", colors.RED),
        onRelease = flashPattern(".", colors.GREEN, nil, false),
        onUnknown = flashPattern("Oooooooo", colors.BLUE, 2),
        onHighlight = flashPattern("OoOoOoOo", colors.WHITE),
        turnOff = flashPattern("O", colors.BLACK),
    }

This code block was replaced with the following:

.. code-block:: c

    _G.MyLed = {
        initial = flashPattern("O", colors.BLACK),
        waitForWifiConnection = flashPattern("O", colors.BLACK),
        invalidSettingsFile = flashPattern("O", colors.BLACK),
        waitForWifiIp = flashPattern("O", colors.BLACK),
        waitForServerConnection = flashPattern("O", colors.BLACK),
        onPreview = flashPattern("O", colors.BLACK),
        onAir = flashPattern("O", colors.RED),
        onRelease = flashPattern("O", colors.BLACK),
        onUnknown = flashPattern("O", colors.BLACK),
        onHighlight = flashPattern("OoOoOoOo", colors.GREEN),
        turnOff = flashPattern("O", colors.BLACK),
    }

Upon each signal the leds will change, but into the BLACK color and into RED when the camera is active.