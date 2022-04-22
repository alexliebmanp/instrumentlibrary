#!/usr/bin/env python3
'''

An example module for defining an instrument class.

@author: Alex Liebman-Pelaez
'''

from . import device

class Instrument(device.Device):

    def __init__(self, name):
        '''Initializes device based on base method.

        args:

            - name: string, device identifier

        For each new instrument the commuication arguments and commands can be specified below as:

            - communication_args: dictionary, communication protocol specifications

            - commands: dictionary, command strings for communicating with device. Each key:value pair should be structured 'Command Description':('Command', Bool), where Bool is true for status commands.
        '''

        ######################
        ## User Input Here ###
        ######################
        # see pyVISA documentation for resource naming conventions: https://pyvisa.readthedocs.io/en/1.8/names.html
        communication_args = {'Protocol':'', 'Address':'1', 'ErrorScheme':'', 'Baud':9600, 'Terminator':''}
        commands = {}
        ######################
        ######################
        ######################

        self.initialize_device(name, communication_args, commands)

        ## any other code you want to run to initialize the device.
