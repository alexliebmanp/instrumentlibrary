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

            - commands: dictionary, command strings for communicating with device.
        '''

        ######################
        ## User Input Here ###
        ######################
        communication_args = {'Protocol':'', 'Address':'1', 'ErrorScheme':'', 'Baud':9600, 'Terminator':''}
        commands = {}
        ######################
        ######################
        ######################

        self.initialize_device(name, communication_args, commands)

        ## any other code you want to run to initialize the device.
