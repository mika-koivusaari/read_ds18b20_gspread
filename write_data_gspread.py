#!/usr/bin/python
import sys
from datetime import date, timedelta
import csv
import re

import gspread
from gspread.exceptions import WorksheetNotFound
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('solar shield data-e15f87bae25f.json', scope)

#gc = gspread.authorize(credentials)
headers = gspread.httpsession.HTTPSession(headers={'Connection':'Keep-Alive'})
gc = gspread.Client(auth=credentials,http_session=headers)
gc.login()

print "Logged in."

filename=None
if len(sys.argv)==2:
  filename=sys.argv[1]
  print "Filename given as argument "+filename
else:
  yesterday = date.today() - timedelta(1)
  filename='data/radiation_shield_%s.csv' % (yesterday.strftime('%Y%m%d'))
  print "No filename given, using "+filename

m = re.match(r".*radiation_shield_(\d{4})(\d{2})(\d{2}).csv", filename)
year=m.group(1)
month=m.group(2)
day=m.group(3)

csvfile=open(filename,'rb')
csvreader=csv.reader(csvfile,delimiter=';')

print "CSV file open."
sheetname=year+'.'+month+'.'+day

#open google sheets
sheet = gc.open_by_key('1V9OOICml3TB_kz-c6pKPEQZLdh8nlp5JI1Lb55njau8')
print "Google Sheet opened."
#try to open todays sheet, if not succesfull then create it 
try:
  wks=sheet.worksheet(sheetname)
  print "Worksheet "+sheetname+" allready exists. Opened."
except WorksheetNotFound:
  wks=sheet.add_worksheet(title=sheetname, rows="1441", cols="5")
  print "Worksheet "+sheetname+" does not exists. Created."

sensors=['28.21CFCE010000','28.79C1CE010000','28.838ECE010000']
values=[]
row=1
col=1

#add header
print "Add header."
wks.update_cell(row,1,'time')
wks.update_cell(row,2,sensors[0])
wks.update_cell(row,3,sensors[1])
wks.update_cell(row,4,sensors[2])

row=row+1

#find the first empty row
print "Find first empty row."
while wks.cell(row,1).value != "":
  row=row+1
if row>2:
  row=row-1
last_time=wks.cell(row,1).value
print "First empty row is "+str(row)+" with value "+last_time

write_data=False

#Worksheet is new, start from beginning
if last_time=="":
  write_data=True

for csvrow in csvreader:
  if last_time==csvrow[0]:
    write_data=True;
    print "Found place in CSV file."
  if write_data:
    cells=wks.range('A'+str(row)+':D'+str(row))

    #set time in row
    cells[0].value=csvrow[0]
    cells[1].value=csvrow[1]
    cells[2].value=csvrow[2]
    cells[3].value=csvrow[3]
    #update all values at once
    wks.update_cells(cells)
    #wks.update_cell(row,1,csvrow[0])
    #wks.update_cell(row,2,csvrow[1])
    #wks.update_cell(row,3,csvrow[2])
    #wks.update_cell(row,4,csvrow[3])
    row=row+1

csvfile.close()

