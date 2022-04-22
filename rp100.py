#!/usr/bin/env python3
'''

Razorbill power supply RP100

@author: Alex Liebman-Pelaez
'''

from . import device

class RP100(device.Device):

    def __init__(self, name):
        '''Initializes device based on base method.

        args:

            - name: string, device identifier

        For each new instrument the commuication arguments and commands can be specified below as:

            - communication_args: dictionary, communication protocol specifications

            - commands: dictionary, command strings for communicating with device.


        Some important constraints for this specific device:
        (1) keep slew rate below 100 V/s
        (2) keep drive within [-20,120] at room temperature and [-200, 200] at 4K
        (3)
        '''

        ######################
        ## User Input Here ###
        ######################
        communication_args = {'Protocol':'Serial_VISA', 'Address':'1', 'ErrorScheme':'', 'Baud':9600, 'Terminator':'\n'}
        commands = {'System clear':'*CLS',
         'Reset device':'*RST',
         'Set output relay on or off':'OUTP# <bool>',
         'Query ouput relay':'OUTP#?',
         'Set output voltage':'SOUR#:VOLT <float>',
         'Query output voltage':'SOUR#:VOLT:NOW?',
         'Query output setpoint':'SOUR#:VOLT?',
         'Set voltage slew rate':'SOUR#:VOLT:SLEW <float>',
         'Query voltage slew rate':'SOUR#:VOLT:SLEW?',
         'Measure output voltage':'MEAS#:VOLT?',
         'Measure output currrent':'MEAS#[:CURR?',
         'Get last error':'SYST:ERR?',
         'Get number of errors':'SYST:ERR:COUN?'}
        ######################
        ######################
        ######################

        self.initialize_device(name, communication_args, commands)

        ## any other code you want to run to initialize the device.

    def set_voltage(self, channel, level):
        '''
            sets voltage level of specific channel at a specific level.
            TODO: limit voltage according to temperature

            args:
                - channel: int, 1 or 2
                - level: float, from -200 to 200
        '''
        min_voltage = -20
        max_voltage = 120

        if min_voltage <= level <= max_voltage:
            self.write(f'SOUR{channel}:VOLT {level}')
            print(f'\n Voltage on Channel {channel} set to {level} V.')
        else:
            print(f'\n Set Voltage outside the acceptable voltage range ({min_voltage}, {max_voltage}).')

    def set_voltage_slew(self, channel, slew_rate):
        '''
            sets voltage slew rate in V/s of specific channel.

            args:
                - channel: int, 1 or 2
                - slew: float, from 0 to 10
        '''
        min_slew = 0
        max_slew = 10

        if min_slew <= slew_rate <= max_slew:
            self.write(f'SOUR{channel}:VOLT:SLEW {slew}')
            print(f'\n Voltage Slew Rate on Channel {channel} set to {slew_rate} V/s.')
        else:
            print(f'\n Set Voltage Slew Rate outside the acceptable voltage range ({min_slew}, {max_slew}).')
