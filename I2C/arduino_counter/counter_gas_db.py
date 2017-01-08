#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : jmaumene
# https://www.maumene.fr
#
# Read Arduino counter and save to DB
# Used to read gaz meter in my home
# One pulse = 0.01 m3
#
# See https://github.com/jmaumene/Arduino/I2C/Arduino_I2C_Counter_Double/Arduino_I2C_Counter_Double.ino
# for arduino sketch
#
# sudo apt-get install python-mysqldb
#

import smbus, sys, time, MySQLdb
from decimal import Decimal

# Set 0 for Raspberry V1, 1 for other
bus = smbus.SMBus(1)

# Counter address
address = 0x12

# Counter to read
counter = 0x01

# Db configuration
DB_HOST="127.0.0.1"
DB_USER="domotique"
DB_PASS="domotique"
DB_BASE="domotique"

# Byte length
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

# Save to DB
def saveToDb(CONSO):
        db = MySQLdb.connect(DB_HOST, DB_USER, DB_PASS, DB_BASE)
        cursor = db.cursor()
        cursor.execute("""INSERT INTO conso_gaz (value)
         VALUES (%s)""" ,(CONSO))
        db.commit()
        db.rollback()
        db.close()

count = read_counter(counter)
count =  Decimal(count) / Decimal(100)

saveToDb(count)

print "Counter : ",count
