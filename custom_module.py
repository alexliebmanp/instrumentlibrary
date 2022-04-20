#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This is a container for elaborating custom communications protocol.

Created on Mon Jun 29 17:22:32 2020

@author: ryanday
"""

class Custom:


    def __init__(self,address):

        self.address = address
        self.connection = self.initialize()

    def initialize(self):
        return 0
