#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 17:16:58 2020

@author: ryanday
"""
import serial

bytesize_dict = {5:serial.FIVEBITS,
                 6:serial.SIXBITS,
                 7:serial.SEVENBITS,
                 8:serial.EIGHTBITS}

parity_dict = {'none':serial.PARITY_NONE,
               'even':serial.PARITY_EVEN,
               'odd':serial.PARITY_ODD,
               'mark':serial.PARITY_MARK,
               'space':serial.PARITY_SPACE}

stop_dict = {1:serial.STOPBITS_ONE,
             1.5:serial.STOPBITS_ONE_POINT_FIVE,
             2:serial.STOPBITS_TWO}

class RS232:

    def __init__(self,comm_args):
        '''
        Instantiate RS232 connection class

        args:

            - comm_args: dictionary of arguments for opening the serial connection.
            Requred keys: "Address", "Baud", "StopBits","ByteSize","Timeout","ErrorScheme"
        '''
        try:
            self.port = comm_args['Address']
        except KeyError:
            raise('Missing "Address" key-value pair for comm-port.')
        try:
            self.baud = comm_args['Baud']
        except KeyError:
            raise('Missing "Baud" key-value pair for comm-port.')
        if 'StopBits' in comm_args:
            try:
                self.stopbits = stop_dict[comm_args['StopBits']]
            except:
                raise('Invalid choice of stop bits. Must be 1,1.5 or 2.')
        else:
            raise('Missing "StopBits" key-value pair for comm-port.')

        if 'ByteSize' in comm_args:
            try:
                self.bytesize = bytesize_dict[comm_args['ByteSize']]
            except:
                raise('Invalid byte size choice. Must be in range (5-8).')
        else:
            raise('Missing "ByteSize" key-value pair for comm-port.')

        if 'Timeout' in comm_args:
            self.timeout = comm_args['Timeout']
        else:
            self.timeout = 2.0

        if 'Termination' in comm_args:
            self.termination = comm_args['Termination']
        else:
            self.termination = '\r\n'

        try:
            self.encoding = comm_args['Encoding']
        except:
            self.encoding = 'utf-8'
        try:
            self.error = self.error_identify(comm_args['ErrorScheme'])
        except:
        #            raise('Missing "ErrorScheme" key-value pair for comm-port.')
            self.error = ('parity',parity_dict['none'])

        self.connection_args = self.connect_config()

    def error_identify(self,args):
        '''
        TODO: this needs to be expanded to go beyond parity-check as the
        error detection scheme.

        '''

        if args[0].lower()=='parity':
            try:
                return ('parity',parity_dict[args[1]])
            except:
                raise('Invalid choice of parity check.')
        else:
            return args

    def connect_config(self):
        '''
        Initialize connection with serial device. Instantiate the
        connection, define essential attributes

        args:

            - port: string, name of COM port

            - baud: int, baud-rate

            - timeout: float, limit on read/write time, in seconds

        return:

            - connection: instance of pyserial's Serial class

        '''



        connection_args = dict(port = self.port,
                               baudrate = self.baud,
                               timeout = self.timeout,
                               bytesize = self.bytesize,
                               stopbits = self.stopbits)
        if self.error[0] == 'parity':
            connection_args['parity'] = self.error[1]

        return connection_args

    def transmit(self,string):

        message = self.build(string)
        self.write(message)

    def build(self,message):

        message_string = message + self.termination
        return message_string.encode(self.encoding)

    def write(self,message):
        '''
        Transmit message over the serial bus

        args:

            - message: string, to be transmitted to device

        '''
        with serial.Serial(**self.connection_args) as connection:
            connection.write(message)

    def query(self,message):
        '''
        Query device status: transmit message, and wait for response.
        A possible error-check is performed as an intermediate step. The system
        is given 3 chances to transmit successfully before an empty-string is
        returned.

        args:

            - message: unicode-string to transmit to device.

        return:

            - readstring: string, received from device.
        '''

        readstring = ''
        success = False
        attempts = 0
        with serial.Serial(**self.connection_args) as connection:
            while attempts < 3:
                if not success:
                    connection.write(message)
                    success = self.do_error_check(connection)
                    attempts+=1

                if success:
                    readstring = str(connection.readline().strip(),self.encoding)
                    if len(readstring)==0:
                        attempts+=1
                        success = False
                    else:
                        return readstring

        return readstring

    def read(self):
        '''
        Read off of the serial bus

        *eturn:

            - linein: raw string read off of the device
        '''
        with serial.Serial(**self.connection_args) as connection:
            linein = connection.readline().strip()
        return str(linein)

    def do_error_check(self,connection):
        '''
        Do the device-specific error check following data transmission.
        If it's a parity check, this is already taken care of. If there is no
        parity bit, for example we have an intermediate confirmation message (I
        call this a handshake) then we do this instead. This needs to be fleshed
        out more to be more comprehensive for different device styles

        *args*:

            - **connection**:instance of pySerial Serial class

        *return*:

            - boolean, True if error check passes successfully
        '''

        if self.error[0] == 'parity':
            return True
        elif self.error[0] == 'handshake':

            error_read = str(connection.readline().strip(),encoding=self.encoding)
            if error_read == self.error[1][0]:
                error_confirm = self.build(self.error[1][1])
                connection.write(error_confirm)
                return True
            else:
                return False
        else:
            return False

#    def open_comm(self):
#        '''
#        Check if communication is open, and if not, open
#
#        '''
#
#        if not self.connection.is_open:
#            self.connection.open()
#
#    def close_comm(self):
#        '''
#        Check if communication is open, and if so, close
#        '''
#        if self.connection.is_open:
#            self.connection.close()
#
