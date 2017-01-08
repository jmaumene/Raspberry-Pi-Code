#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : jmaumene
# https://www.maumene.fr
#
# Read Arduino counter
#
# See https://github.com/jmaumene/Arduino/I2C/Arduino_I2C_Counter_Double/Arduino_I2C_Counter_Double.ino
# for arduino sketch

import smbus, sys, time

# Set 0 for Raspberry V1, 1 for other
bus = smbus.SMBus(1)

# counter address
address = 0x12

# byte length
byte_length = 4

# Read
def read_counter(counter):
  data = []
  cpt = 0

  bus.write_byte(address, counter)
  while cpt < byte_length:
    time.sleep(0.05)
    data.append(bus.read_byte(address) << 8*cpt)
    #print "Read ", data[cpt]
    cpt += 1

  return sum(data)

if len(sys.argv) == 2:
  data = read_counter(int(sys.argv[1]))
  print "Counter : ",data

else:
  print "set counter 1 OR 2"

