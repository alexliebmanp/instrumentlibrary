#!/usr/bin/env python3
'''
@author: ryanday
@modified: Alex Liebman-Pelaez <oxide>
@date:   2022-04-20T09:24:11-07:00
'''

import datetime as dt
import time
from . import gpib_module as gpib
from . import serial_module as serial
from . import custom_module as custom
from . import serial_visa_module as serial_visa

class Device:

    '''
    Device is the template for an instrument or device that communicates over some communications protocol, sends messages, and receives replies. It can accommodate connections to devices over a variety of communication protocols, including RS-232, GPIB/HPIB.

    The command structure for each device may differ, as do the content of the communication strings sent over the wire. Standard error detection protocols are provided, as is device-specific expression.

    All available communication strings are stored in a dictionary with key:value pairs corresponding to a Plain Text name for the command saved with with associated command-string.

    A typical byte string is going to include:

        - command identifier, command argument, error detection code, termination


    The connection args will be a dictionary. It will contain the key:value pairs

        Protocol: string, 'RS232','GPIB',...
        Address: string, name of com-port
        ErrorScheme: ... details of error detection scheme for device
        Baud: int
        Terminator: char

    TODO: implement a way to translate between Plain Text commands and command-strings so that the argument to write can be human readable.


    '''
    def __init__(self):
            return 0

    def initialize_device(self,name,communication_args,commands):
        '''
        Instantiate the device class. User passes a device identifier,
        in addition to requisite arguments to establish communication protocol, as well as the commands of interest. The values for commands are mixed tuple of string and boolean, indicating the device query-string, and whether or not the command is desired for monitoring.

        args:

            - name: string, device identifier

            - communication_args: dictionary, communication protocol specifications

            - commands: dictionary, command strings for communicating with device.

        '''


        self.name = name
        self.connection = self.initialize_connection(communication_args)
        self.CommandTable,self.StatusCommands,self.Status = self.instantiate_commands(commands)


    def initialize_connection(self,connection_args):
        '''
        Establish connection with device. Set up communication.

        args:

            - connection_args: dictionary

        return:

            - connection: virtual connection object, establishing communication with device

        '''

        if connection_args['Protocol'] == 'GPIB':
            connection = gpib.GPIB(connection_args)
        elif connection_args['Protocol'] == 'RS232':
            connection = serial.RS232(connection_args)
        elif connection_args['Protocol'] == 'Serial_VISA':
            connection = serial_visa.Serial(connection_args)
        else:
            print('LCMI is not familiar with the {:s} protocol. You will have to give us more information.'.format(connection_args['Protocol']))
            connection = custom.Custom(connection_args)

        return connection

    def close_connection(self):

        return self.connection.close()

    def instantiate_commands(self,all_commands):

        '''
        Set up dictionaries detailing all defined commands, as well as those
        specifically relevant to status updates, and a container for status
        information to be stored.

        args:

            - all_commands: dictionary of string:string pairs with plain text label, and command string to be sent to device.

        return:

            - CommandTable: dictionary of all commands

            - StatusCommands: dictionary, subset of all commands relevant to status updates

            - Status: dictionary, container for status information in string format

        '''

        CommandTable = {}
        StatusCommands = {}
        Status = {'DateTime':dt.datetime.now()}

        for ci in all_commands:
            CommandTable[ci] = all_commands[ci][0]
            if all_commands[ci][1]:
                StatusCommands[ci] = all_commands[ci][0]
                Status[ci] = None

        return CommandTable,StatusCommands,Status

    def get_status(self):

        '''
        Iterate through all requisite status commands and query the instrument.
        Time of query is also recorded (once for the entire set of readings).

        '''
        self.Status['DateTime'] = dt.datetime.now().strftime('%H:%M:%S %d/%m/%y')
        for command in self.StatusCommands:
            writestring = self.connection.build(self.StatusCommands[command])
            self.Status[command] = self.connection.query(writestring)

    def print_commands(self):
        '''
        Print summary of the CommandTable attribute, organized as a table of key value pairs
        '''
        print('\n'.join(['| {:s} | {:s} |'.format(si,self.CommandTable[si]) for si in self.CommandTable]))

    def print_statcomms(self):

        '''
        Print summary of the StatusCommands attribute, organized as a table of key value pairs
        '''
        print('\n'.join(['| {:s} | {:s} |'.format(si,self.StatusCommands[si]) for si in self.StatusCommands]))

    def print_status(self):

        '''
        Print current device status, as last queried.
        TODO: this is not safe against different key-value types, must all be formatted as strings
        '''
        print('\n'.join([' {:s} | {:s} |'.format(si,self.Status[si]) for si in self.Status]))

    def write(self,message):

        return self.connection.write(message)

    def read(self):

        return self.connection.read()

    def query(self, query_message):

        return self.connection.query(query_message)
