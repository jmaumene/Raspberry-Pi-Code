#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : jmaumene
#
# Get device from mysal database and insert temperature
#
# sudo apt-get install python-mysqldb
#

import glob
import time
import sys
import MySQLdb
import datetime
import os.path

DB_HOST="127.0.0.1"
DB_USER="domotique"
DB_PASS="domotique"
DB_BASE="domotique"


def getFromDB():
        db = MySQLdb.connect(DB_HOST, DB_USER, DB_PASS, DB_BASE)
        cursor = db.cursor()
        cursor.execute("SELECT device, name FROM w1_device WHERE type = 'temp' && active = 1")
        rows = cursor.fetchall()
        for row in rows:
                TEMP = read_1wire(row[0])
                print ' Temperature Sonde ', row[1], 'device: ', row[0] ,' : ', TEMP, 'degre'
                if TEMP:
                        saveToDb(row[0], TEMP)

def read_1wire_raw(file_device):
        if os.path.isfile(file_device):
                f = open(file_device, 'r')
                lines = f.readlines()
                f.close()
                return lines
        return False

def read_1wire(device):
        file_device = '/sys/bus/w1/devices/' + device + '/w1_slave';
        if os.path.isfile(file_device):
                lines = read_1wire_raw(file_device)
                while lines[0].strip()[-3:] != 'YES':
                        time.sleep(0.1)
                        lines = read_1wire_raw(file_device)
                equals_pos = lines[1].find('t=')
                if equals_pos != -1:
                        temp_string = lines[1][equals_pos+2:]
                        temp_c = float(temp_string) / 1000.0
                        return temp_c
        return False

def saveToDb(DEVICE, TEMP):
        # INSERT NEW TEMP
        db = MySQLdb.connect(DB_HOST, DB_USER, DB_PASS, DB_BASE)
        cursor = db.cursor()
        cursor.execute("""INSERT INTO w1_temp (device, value)
         VALUES (%s, %s)""" ,(DEVICE, TEMP))
        # send to database
        db.commit()
        db.rollback()
        db.close()

getFromDB()

