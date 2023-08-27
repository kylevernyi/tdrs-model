# tdrs-model
Fun micropython script to add blinking lights and temperature sensing to TDRS satellite model. Runs on Raspberry Pi Pico.

## Flashing
Micropython makes it very easy to flash code to the Pico. Just rename your Python script `main.py`, connect the Pico to your PC with USB, and drag and drop the `main.py` file. 

## Some notes
- Could not get broadcast/multicast to work on the python networking module. It may not be supported on the Micropython side
- Temperature data from the onboard temperature sensor is streamed to `192.168.1.168:5005` and can be received with the `recv.py` script.
- replace the SSID and Password with your wifi information
