#!/usr/bin/python
import sys
import time

import gspread
from gspread.exceptions import WorksheetNotFound
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('solar shield data-e15f87bae25f.json', scope)

gc = gspread.authorize(credentials)

_time=time.strftime('%H:%M')
_date=time.strftime('%d.%m')

#open google sheets
sheet = gc.open_by_key('1V9OOICml3TB_kz-c6pKPEQZLdh8nlp5JI1Lb55njau8')
#try to open todays sheet, if not succesfull then create it 
try:
  wks=sheet.worksheet(_date)
except WorksheetNotFound:
  wks=sheet.add_worksheet(title=_date, rows="1441", cols="5")

sensors=['28.21CFCE010000','28.79C1CE010000','28.838ECE010000']
values=[]
row=1
col=1

#check first row to see if there is a header
value=wks.cell(row,col).value
if value=='':
  wks.update_cell(row,1,'time')
  wks.update_cell(row,2,sensors[0])
  wks.update_cell(row,3,sensors[1])
  wks.update_cell(row,4,sensors[2])

#find which row is first empty
while wks.cell(row,1).value!='':
  row=row+1

owfspath='/var/1-wire/mnt/1F.BD5C08000000/aux/'

#set time in row
wks.update_cell(row,col,_time)
col=col+1

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
#print ''

#write values to google sheet
for value in values:
  wks.update_cell(row,col,'%0.4f' % (value))
  col=col+1


