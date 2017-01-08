#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : jmaumene
# https://www.maumene.fr
#
# Read Arduino counter
#
# See https://github.com/jmaumene/Arduino/I2C/Arduino_I2C_Counter_Double/Arduino_I2C_Counter_Double.ino
# for arduino sketch

import smbus, time, os, sys

# Set 0 for Raspberry V1, 1 for other
bus = smbus.SMBus(1)
address = 0x12
data = []

if len(sys.argv) == 3:
  cmd = int(sys.argv[1]) + 2
  counter = int(sys.argv[2])

  data.append(counter & 0xfF);
  data.append((counter >> 8) & 0xff);
  data.append((counter >> 16) & 0xff);
  data.append((counter >> 24) & 0xff);

  bus.write_block_data(address, cmd, data)
  time.sleep(0.01)
  result = bus.read_byte(address)
  print 'write : ', counter
  # print 'result : ',result
else:
  print "Error:  write.py 1 1234567"
