#!/usr/bin/python
import sys
import time

_time=time.strftime('%H:%M')

sensors=['28.21CFCE010000','28.79C1CE010000','28.838ECE010000']
values=[]

owfspath='/var/1-wire/mnt/1F.BD5C08000000/aux/'

#write to simultaneous so all sensors do their conversion at the same time
#all sensors in the bus need to be externally powered! Parasitic sensors can only convert one at a time!
f=open(owfspath+'simultaneous/temperature','w')
f.write('1')
f.close()

#loop all sensors and put their values in a list
for sensor in sensors:
  try:
    f=open(owfspath+sensor+'/temperature','r')
    value=f.readline()
    valuef=float(value)
#    sys.stdout.write('%0.4f, ' % (valuef))
    values.append(valuef)
  except IOError:
    print "sensor not found ",owfspath+sensor
print '%s;%0.4f;%0.4f;%0.4f' % (values[0],values[1],values[2])
