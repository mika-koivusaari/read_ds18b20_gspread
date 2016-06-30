#!/usr/bin/python
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('solar shield data-e15f87bae25f.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open_by_key('1V9OOICml3TB_kz-c6pKPEQZLdh8nlp5JI1Lb55njau8').sheet1

sensors=('28.21CFCE010000','28.79C1CE010000','28.838ECE010000')
owfspath='/var/1-wire/mnt/1F.BD5C08000000/aux/'

f=open(owfspath+'simultaneous/temperature','w')
f.write('1')
f.close()
row=1
col=1
for sensor in sensors:
  try:
    f=open(owfspath+sensor+'/temperature','r')
    value=f.readline()
    valuef=float(value)
    sys.stdout.write('%0.4f, ' % (valuef))
    wks.update_cell(row,col,value)
    col=col+1
#    sys.stderr.write("id=%i value='%s'\n" % (record[0],value))
#    cursor.execute("INSERT INTO data (sensorid,time,value) VALUES (%s,now(), truncate(%s,2))",(record[0],value.lstrip()))
  except IOError:
    print "sensor not found ",owfspath+sensor
print ''

