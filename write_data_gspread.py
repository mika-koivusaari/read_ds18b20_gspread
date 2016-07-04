#!/usr/bin/python
import sys
from datetime import date, timedelta
import csv

import gspread
from gspread.exceptions import WorksheetNotFound
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('solar shield data-e15f87bae25f.json', scope)

gc = gspread.authorize(credentials)

filename=None
if len(sys.argv)==2:
  filename=sys.argv[1]
else:
  exit(1)
  #yesterday = date.today() - timedelta(1)
  #_date=.strftime('%d.%m')

csvfile=open(filename,'rb')
csvreader=csv.reader(csvfile,delimiter=';')

sheetname='testi'

#open google sheets
sheet = gc.open_by_key('1V9OOICml3TB_kz-c6pKPEQZLdh8nlp5JI1Lb55njau8')
#try to open todays sheet, if not succesfull then create it 
try:
  wks=sheet.worksheet(sheetname)
except WorksheetNotFound:
  wks=sheet.add_worksheet(title=sheetname, rows="1441", cols="5")

sensors=['28.21CFCE010000','28.79C1CE010000','28.838ECE010000']
values=[]
row=1
col=1

#add header
wks.update_cell(row,1,'time')
wks.update_cell(row,2,sensors[0])
wks.update_cell(row,3,sensors[1])
wks.update_cell(row,4,sensors[2])

row=row+1

for csvrow in csvreader:
  #set time in row
  wks.update_cell(row,1,csvrow[0])
  wks.update_cell(row,2,csvrow[1])
  wks.update_cell(row,3,csvrow[2])
  wks.update_cell(row,4,csvrow[3])
  row=row+1

csvfile.close()

