#!/usr/bin/python
import sys

sensors=('28.21CFCE010000','28.79C1CE010000','28.838ECE010000')
owfspath='/var/1-wire/mnt/1F.BD5C08000000/aux/'

f=open(owfspath+'simultaneous/temperature','w')
f.write('1')
f.close()
for sensor in sensors:
  try:
    f=open(owfspath+sensor+'/temperature','r')
    value=f.readline()
    print "sensor",sensor,value
#    sys.stderr.write("id=%i value='%s'\n" % (record[0],value))
#    cursor.execute("INSERT INTO data (sensorid,time,value) VALUES (%s,now(), truncate(%s,2))",(record[0],value.lstrip()))
  except IOError:
    print "sensor not found ",owfspath+sensor
