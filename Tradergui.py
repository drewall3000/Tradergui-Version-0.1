import yahoo_finance
from yahoo_finance import *
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import datetime
SPYPATTERNS=pd.read_csv('SPYPATTERNS.csv', sep='\t')
SPYPATTERNS=DataFrame(SPYPATTERNS)
SPY = Share('SPY')
#year-month-day
TODAY=datetime.date.today()
WEEKDAYVALUE=TODAY.weekday()
if WEEKDAYVALUE<4:
	FIVEDAYSAGO=TODAY-datetime.timedelta(days=7)
elif WEEKDAYVALUE==4:
	FIVEDAYSAGO=TODAY-datetime.timedelta(days=5)
TODAY=TODAY.isoformat()
FIVEDAYSAGO=FIVEDAYSAGO.isoformat()
LASTFIVEDAYS=SPY.get_historical(FIVEDAYSAGO,TODAY)
LASTFIVEDAYS=DataFrame(LASTFIVEDAYS)
CLOSE=DataFrame(LASTFIVEDAYS['Close'])
OPEN=DataFrame(LASTFIVEDAYS['Open'])
#Create an empty dataframe to fill with last five day pattern
index=len(OPEN)
columns=['Pattern']
SPYPATTERN=[]*5

def plusminus():
	a=0
	y=0
	for i in range (5):
		if CLOSE.iloc[a,y] > OPEN.iloc[a,y]:
			SPYPATTERN[a:a]='+'
		elif CLOSE.iloc[a,y] < OPEN.iloc[a,y]:
			SPYPATTERN[a:a]='-'
		else:
			SPYPATTERN[a:a]='NEUT'

		a+=1
plusminus()
SPYPATTERN=DataFrame(SPYPATTERN,columns=['PATTERN'])
SPYPATTERN=[SPYPATTERN['PATTERN'].apply(str)[0],SPYPATTERN['PATTERN'].apply(str)[1],
SPYPATTERN['PATTERN'].apply(str)[2],SPYPATTERN['PATTERN'].apply(str)[3],
SPYPATTERN['PATTERN'].apply(str)[4]]
SPYPATTERN=''.join(SPYPATTERN)
a=0
NOMATCH=0
up=0
down=0
while NOMATCH==0:
	if SPYPATTERN==SPYPATTERNS.iloc[a,0]:
		up=SPYPATTERNS.iloc[a,3]
		dwn=SPYPATTERNS.iloc[a,4]
		NOMATCH=1
	else:
		NOMATCH=0
	a+=1

print (" ")
print ("Last five days the SPY has done the following:")
print (SPYPATTERN)
up='{0:.0%}'.format(up)
print ("Percent of days up following the above pattern:")
print (up)
dwn='{0:.0%}'.format(dwn)
print ("Percent of days down following the above pattern:")
print (dwn)
print ("SPY data tested from 1/29/1993 to 3/11/2016")
print (" ")
'''
Tradergui=tkinter.Tk()

Tradergui.mainloop()
'''