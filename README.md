Orenstein Lab Instrument Library

This code streamlines the process of introducing a new device into the Orenstein Lab python environment, allowing user to specify all device-specific instructions for communication. It is basically a convenient wrapper for a number of python libraries such as pyVISA and pySerial.

Dependencies: pyvisa, pyvisa-py, pyserial

At the core of this library is the generic Device class, which establishes communication via desired comm protocol with the device, keeps a dictionary of commands, and reads/writes to the device. Actual instruments are then implemented via subclasses, which are written in the image of 'instrument_template'. The user provides information on the communication standards and the commands (eg, SPCI commands), and with a few lines of code gain access to the instrument.

User responsibilities:

- identify device's comm-protocol (e.g. RS232, GPIB, etc)
- identify command format (e.g. error correction bit, string length, termination characters, etc)
- identify device comm-port
- identify all relevant device queries (e.g. temperature query, voltage measurement, etc)

Envisioned workflow:
(1) Write a new device class in a separate module (eg, keithlyXYZ.py contains the KeithlyXCY class)
(2) import KeithlyXYZ into a specific application and use, for example:

from instrumentlibrary import keithlyXYZ as kth

current_source = kth.KeithlyXCZ.(address) # initializes the connection
current_source.write('Set Current', 1)
