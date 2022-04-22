#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 17:16:35 2020

@author: ryanday
"""
import pyvisa as visa

class GPIB:

    def __init__(self,communication_args):
        '''Instantiate the GPIB connection. We use the pyvisa package for communication via GPIB.

        args:

        - communication_args: dictionary

        '''
        self.ResourceManager = visa.ResourceManager('@py')
        self.address = communication_args['Address']
        self.termination = ''
        self.connection = self.connect()

    def connect(self):
        '''Establish connection with device at designated location.

        return:

        - connection: communication connection '''

        connection = self.ResourceManager.open_resource(self.address)
        return connection

    def close(self):
        '''Close and disconnection the communication line with device.
        '''

        self.connection.before_close()
        self.connection.close()


    def build(self,message):
        '''Buile a message string with correct termination
        '''

        message_string = message + self.termination

        return message_string

    def query(self,query):
        '''Combined write-read command. If device fails to return anything (e.g. no connection),
        this returns an empty string

        args:

        - query: string, question to transmit to device, requesting information

        return:

        - message: string, response from device
        '''
        try:
            message = self.connection.query(query).strip()
        except:
            message = ''
        return message

    def write(self, message):
        '''Write message to device.
        args:

           - message: string, message for device.'''

        self.connection.write(message)

    def read(self):
        '''Read data off the bus. Return empty string if read() raises an error (e.g. no device)

        return:

           - message: string, data from device.
        '''
        try:
           message = self.connection.read().strip()
        except:
           message = ''
        return message

class Serial:

    def __init__(self,communication_args):
        '''Instantiate the Serial connection. We use the pyvisa package for communication via a virtual comm port (ie not directly accessing the comm port). Main difference from GPIB module is the addition of a terminator. In the future, I could think about combining these two kinds of

        args:

        - communication_args: dictionary

        '''
        self.ResourceManager = visa.ResourceManager('@py')
        self.address = communication_args['Address']
        self.termination = communication_args['Terminator']
        self.connection = self.connect()

    def connect(self):
        '''Establish connection with device at designated location.

        return:

        - connection: communication connection '''

        connection = self.ResourceManager.open_resource(self.address)
        return connection

    def close(self):
        '''Close and disconnection the communication line with device.
        '''

        self.connection.before_close()
        self.connection.close()


    def build(self,message):
        '''Buile a message string with correct termination
        '''

        message_string = message + self.termination

        return message_string

    def query(self,query):
        '''Combined write-read command. If device fails to return anything (e.g. no connection),
        this returns an empty string

        args:

        - query: string, question to transmit to device, requesting information

        return:

        - message: string, response from device
        '''
        try:
            message = self.connection.query(self.build(query)).strip()
        except:
            message = ''
        return message

    def write(self, message):
        '''Write message to device.
        args:

           - message: string, message for device.'''

        self.connection.write(self.build(message))

    def read(self):
        '''Read data off the bus. Return empty string if read() raises an error (e.g. no device)

        return:

           - message: string, data from device.
        '''
        try:
           message = self.connection.read().strip()
        except:
           message = ''
        return message
