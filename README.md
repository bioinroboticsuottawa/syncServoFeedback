Servo with Feedback sync communication
======================================

A simple implementation of sync communication between arduino and python code.

Our servo was modified to have a signal feedback from its internal potentiometer. The voltage is sent to python code in a burst mode.

The Python script sends a burst size to arduino. When Arduino receive this value it makes measurements of servo potentiometer voltage, sending back to python and waiting for another request.

Another serial communication in python script is made with SSC-32 board to control servo position. In this way we have a feedback of servo position according to potentiometer voltage and servo position adjustment by SSC-32 board.

Installation
------------

Upload Arduino code to your board and (if necessary) change serial port definition in python script.
