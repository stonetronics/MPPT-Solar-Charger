# Raspberry Pi python readout of the MPPT-Solar-Charger

This example showcases readout of the MPPT-Solar-Charger from a Raspberry Pi using python.
It is written in a way that outputs all of measurement and status data in json format, so it can easily be further processed by higher level services like Node-Red.

The example was tested using a Raspberry Pi Zero W, connected to SDA (GPIO2), SCL(GPIO3), GND and +5V.