import os
import pandas as pd
import pymysql.cursors
from pandas import DataFrame
import Quandl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import datetime
from datetime import date
import sqlite3
import requests
import bs4
from bs4 import BeautifulSoup
import csv

#IMPORT CSVS

SPYPATTERNS=pd.read_csv(os.path.expanduser("~/Documents/Python/SPYPATTERNS.csv"), sep='\t')
SPYPATTERNS=DataFrame(SPYPATTERNS)
ESWEEKLYPATTERNS=pd.read_csv(os.path.expanduser("~/Documents/Python/ESWEEKLYPATTERNS.csv"), sep='\t')
ESWEEKLYPATTERNS=DataFrame(ESWEEKLYPATTERNS)
HIGHLOWPATTERNSDF=pd.read_csv(os.path.expanduser("~/Documents/Python/FINALRESULTSALL.csv"), sep='\t')
HIGHLOWPATTERNSDF=DataFrame(HIGHLOWPATTERNSDF)
HIGHLOWWEEK=pd.read_csv(os.path.expanduser("~/Documents/Python/FINALRESULTSWEEK.csv"), sep='\t')
HIGHLOWWEEK=DataFrame(HIGHLOWWEEK)

#RETREIVE LAST FIVE WEEKS FROM QUANDL

ES = Quandl.get("CHRIS/CME_ES1",authtoken="vGe9xLEuwzZcGy68aEot")
ESNOW = Quandl.get("CME/ESM2016", authtoken="vGe9xLEuwzZcGy68aEot")
CLNOW=DataFrame(ESNOW['Last'])
CLNOW=CLNOW.iloc[::-1]
OPDAY=DataFrame(ES['Open'])
HIDAY=DataFrame(ES['High'])
LODAY=DataFrame(ES['Low'])
CLDAY=DataFrame(ES['Last'])

#REVERSE ORDER OF DataFrame

OPDAY=OPDAY.iloc[::-1]
HIDAY=HIDAY.iloc[::-1]
LODAY=LODAY.iloc[::-1]
CLDAY=CLDAY.iloc[::-1]
OPDAY.reset_index(level=0, inplace=True)
CLDAY.reset_index(level=0, inplace=True)
HIDAY.reset_index(level=0, inplace=True)
LODAY.reset_index(level=0, inplace=True)

#fill dataframe with weekday numbers
#finding edge cases when market not open

weekdaynumsDF=DataFrame([0]*len(OPDAY))
def weekdaynums():
    x=0
    while x<=(len(OPDAY)-1):
        weekdaynumsDF.iloc[x,0]=OPDAY.iloc[x,0].weekday()
        x+=1
weekdaynums()

#create histogram of all cases of weekday numbers
#SEPARATE DATA INTO WEEKS BC QUANDL DOESNT DO THIS

if OPDAY.iloc[0,0].weekday()==0:
    OPDAY=OPDAY.ix[1::]
    HIDAY=HIDAY.ix[1::]
    LODAY=LODAY.ix[1::]
    CLDAY=CLDAY.ix[1::]
if OPDAY.iloc[0,0].weekday()==1:
    if OPDAY.iloc[1,0].weekday()==4:
        OPDAY=OPDAY.ix[1::]
        HIDAY=HIDAY.ix[1::]
        LODAY=LODAY.ix[1::]
        CLDAY=CLDAY.ix[1::]
    else:
        OPDAY=OPDAY.ix[2::]
        HIDAY=HIDAY.ix[2::]
        LODAY=LODAY.ix[2::]
        CLDAY=CLDAY.ix[2::]
if OPDAY.iloc[0,0].weekday()==2:
    if OPDAY.iloc[2,0].weekday()==4:
        OPDAY=OPDAY.ix[2::]
        HIDAY=HIDAY.ix[2::]
        LODAY=LODAY.ix[2::]
        CLDAY=CLDAY.ix[2::]
    else:
        OPDAY=OPDAY.ix[3::]
        HIDAY=HIDAY.ix[3::]
        LODAY=LODAY.ix[3::]
        CLDAY=CLDAY.ix[3::]
if OPDAY.iloc[0,0].weekday()==3:
    if OPDAY.iloc[3,0].weekday()==4:
        OPDAY=OPDAY.ix[3::]
        HIDAY=HIDAY.ix[3::]
        LODAY=LODAY.ix[3::]
        CLDAY=CLDAY.ix[3::]
    else:
        OPDAY=OPDAY.ix[4::]
        HIDAY=HIDAY.ix[4::]
        LODAY=LODAY.ix[4::]
        CLDAY=CLDAY.ix[4::]


OPWEEK=DataFrame([0]*5)
CLWEEK=DataFrame([0]*5)

weekHI=DataFrame([0]*5)
weekLO=DataFrame([0]*5)
week2HI=DataFrame([0]*5)
week2LO=DataFrame([0]*5)
week3HI=DataFrame([0]*5)
week3LO=DataFrame([0]*5)
week4HI=DataFrame([0]*5)
week4LO=DataFrame([0]*5)
week5HI=DataFrame([0]*5)
week5LO=DataFrame([0]*5)
WK1HI=0
WK1LO=0
WK2HI=0
WK2LO=0
WK3HI=0
WK3LO=0
WK4HI=0
WK4LO=0
WK5HI=0
WK5LO=0
#Redoing week OHLC bc I couldn't make sense of what to do with existing code
#Getting rid of functions and using OHLC format for clarity longer but clearer
#Checks for Mon and Fri off days
TODAY=date.today()
def POPWEEKS():
    x=0
    y=1
    z=2
    a=3
    b=4
    c=5
    d=0
    edgeCASE=0
    while c<=25:
        if OPDAY.iloc[x,0].weekday()==4:
            if OPDAY.iloc[b,0].weekday()==0:
                OPWEEK.iloc[d,0]=OPDAY.iloc[b,1]
                weekHI.iloc[d,0]=HIDAY.iloc[x:c,1].max()
                weekLO.iloc[d,0]=LODAY.iloc[x:c,1].min()
                CLWEEK.iloc[d,0]=CLDAY.iloc[x,1]
            else:
                OPWEEK.iloc[d,0]=OPDAY.iloc[a,1]
                weekHI.iloc[d,0]=HIDAY.iloc[x:b,1].max()
                weekLO.iloc[d,0]=LODAY.iloc[x:b,1].min()
                CLWEEK.iloc[d,0]=CLDAY.iloc[x,1]
                #adding edge case counter to shorten variables below bc DF is shortened by one day
                edgeCASE+=1
        if OPDAY.iloc[x,0].weekday()==3:
            OPWEEK.iloc[d,0]=OPDAY.iloc[a,1]
            weekHI.iloc[d,0]=HIDAY.iloc[x:b,1].max()
            weekLO.iloc[d,0]=LODAY.iloc[x:b,1].min()
            CLWEEK.iloc[d,0]=CLDAY.iloc[x,1]
            edgeCASE+=1

        x+=5-edgeCASE
        y+=5-edgeCASE
        z+=5-edgeCASE
        a+=5-edgeCASE
        b+=5-edgeCASE
        c+=5-edgeCASE
        d+=1
        #reset edge case so not repeated next loop
        edgeCASE=0

POPWEEKS()
#need to fix this so that off mondays and fridays edge cases are recognized

#saving results from above in separate variables for some reason and saving them in a new dataframe makes no sense
WK1HI=weekHI.iloc[0,0]
WK1LO=weekLO.iloc[0,0]
WK2HI=weekHI.iloc[1,0]
WK2LO=weekLO.iloc[1,0]
WK3HI=weekHI.iloc[2,0]
WK3LO=weekLO.iloc[2,0]
WK4HI=weekHI.iloc[3,0]
WK4LO=weekLO.iloc[3,0]
WK5HI=weekHI.iloc[4,0]
WK5LO=weekLO.iloc[4,0]
HIWKFIVE=DataFrame([WK1HI,WK2HI,WK3HI,WK4HI,WK5HI])
LOWKFIVE=DataFrame([WK1LO,WK2LO,WK3LO,WK4LO,WK5LO])

#Save last five weeks in DOPWKFIVE=OPWEEK.iloc[0:6]

#test for the high low week pattern
TWOWEEKPATTERN=['0']*2
TWOWEEKPATTERN=DataFrame(TWOWEEKPATTERN, columns=['TWOWEEKPATTERN'])

def TWOWEEK():
    x=0
    y=1
    if HIWKFIVE.iloc[x,0]>HIWKFIVE.iloc[y,0]:
        TWOWEEKPATTERN.iloc[x,0]='HH'
    elif HIWKFIVE.iloc[x,0]<HIWKFIVE.iloc[y,0]:
        TWOWEEKPATTERN.iloc[x,0]='LH'
    if LOWKFIVE.iloc[x,0]<LOWKFIVE.iloc[y,0]:
        TWOWEEKPATTERN.iloc[y,0]='LL'
    elif LOWKFIVE.iloc[x,0]>LOWKFIVE.iloc[y,0]:
        TWOWEEKPATTERN.iloc[y,0]='HL'
    if HIWKFIVE.iloc[x,0]==HIWKFIVE.iloc[y,0]:
        TWOWEEKPATTERN.iloc[x,0]='00'
    if LOWKFIVE.iloc[x,0]==LOWKFIVE.iloc[y,0]:
        TWOWEEKPATTERN.iloc[y,0]='00'
TWOWEEK()
TWOWEEKPATTERN=[TWOWEEKPATTERN['TWOWEEKPATTERN'].apply(str)[0],
TWOWEEKPATTERN['TWOWEEKPATTERN'].apply(str)[1]]
TWOWEEKPATTERN=''.join(TWOWEEKPATTERN)

THREEWEEKPATTERN=['0']*2
THREEWEEKPATTERN=DataFrame(THREEWEEKPATTERN, columns=['THREEWEEKPATTERN'])

def THREEWEEK():
    z=0
    x=1
    y=2
    if HIWKFIVE.iloc[x,0]>HIWKFIVE.iloc[y,0]:
        THREEWEEKPATTERN.iloc[z,0]='HH'
    elif HIWKFIVE.iloc[x,0]<HIWKFIVE.iloc[y,0]:
        THREEWEEKPATTERN.iloc[z,0]='LH'
    if LOWKFIVE.iloc[x,0]<LOWKFIVE.iloc[y,0]:
        THREEWEEKPATTERN.iloc[x,0]='LL'
    elif LOWKFIVE.iloc[x,0]>LOWKFIVE.iloc[y,0]:
        THREEWEEKPATTERN.iloc[x,0]='HL'
    if HIWKFIVE.iloc[x,0]==HIWKFIVE.iloc[y,0]:
        THREEWEEKPATTERN.iloc[z,0]='00'
    if LOWKFIVE.iloc[x,0]==LOWKFIVE.iloc[y,0]:
        THREEWEEKPATTERN.iloc[x,0]='00'

THREEWEEK()
THREEWEEKPATTERN=[THREEWEEKPATTERN['THREEWEEKPATTERN'].apply(str)[0],
THREEWEEKPATTERN['THREEWEEKPATTERN'].apply(str)[1]]
THREEWEEKPATTERN=''.join(THREEWEEKPATTERN)
THREEWEEKPATTERN=THREEWEEKPATTERN+TWOWEEKPATTERN

FOURWEEKPATTERN=['0']*2
FOURWEEKPATTERN=DataFrame(FOURWEEKPATTERN, columns=['FOURWEEKPATTERN'])

def FOURWEEK():
    z=0
    a=1
    x=2
    y=3
    if HIWKFIVE.iloc[x,0]>HIWKFIVE.iloc[y,0]:
        FOURWEEKPATTERN.iloc[z,0]='HH'
    elif HIWKFIVE.iloc[x,0]<HIWKFIVE.iloc[y,0]:
        FOURWEEKPATTERN.iloc[z,0]='LH'
    if LOWKFIVE.iloc[x,0]<LOWKFIVE.iloc[y,0]:
        FOURWEEKPATTERN.iloc[a,0]='LL'
    elif LOWKFIVE.iloc[x,0]>LOWKFIVE.iloc[y,0]:
        FOURWEEKPATTERN.iloc[a,0]='HL'
    if HIWKFIVE.iloc[x,0]==HIWKFIVE.iloc[y,0]:
        FOURWEEKPATTERN.iloc[z,0]='00'
    if LOWKFIVE.iloc[x,0]==LOWKFIVE.iloc[y,0]:
        FOURWEEKPATTERN.iloc[a,0]='00'

FOURWEEK()
FOURWEEKPATTERN=[FOURWEEKPATTERN['FOURWEEKPATTERN'].apply(str)[0],
FOURWEEKPATTERN['FOURWEEKPATTERN'].apply(str)[1]]
FOURWEEKPATTERN=''.join(FOURWEEKPATTERN)
FOURWEEKPATTERN=FOURWEEKPATTERN+THREEWEEKPATTERN

FIVEWEEKPATTERN=['0']*2
FIVEWEEKPATTERN=DataFrame(FIVEWEEKPATTERN, columns=['FIVEWEEKPATTERN'])

def FIVEWEEK():
    z=0
    a=1
    y=3
    b=4
    if HIWKFIVE.iloc[y,0]>HIWKFIVE.iloc[b,0]:
        FIVEWEEKPATTERN.iloc[z,0]='HH'
    elif HIWKFIVE.iloc[y,0]<HIWKFIVE.iloc[b,0]:
        FIVEWEEKPATTERN.iloc[z,0]='LH'
    if LOWKFIVE.iloc[y,0]<LOWKFIVE.iloc[b,0]:
        FIVEWEEKPATTERN.iloc[a,0]='LL'
    elif LOWKFIVE.iloc[y,0]>LOWKFIVE.iloc[b,0]:
        FIVEWEEKPATTERN.iloc[a,0]='HL'
    if HIWKFIVE.iloc[y,0]==HIWKFIVE.iloc[z,0]:
        FIVEWEEKPATTERN.iloc[z,0]='00'
    if LOWKFIVE.iloc[y,0]==LOWKFIVE.iloc[b,0]:
        FIVEWEEKPATTERN.iloc[a,0]='00'

FIVEWEEK()
FIVEWEEKPATTERN=[FIVEWEEKPATTERN['FIVEWEEKPATTERN'].apply(str)[0],
FIVEWEEKPATTERN['FIVEWEEKPATTERN'].apply(str)[1]]
FIVEWEEKPATTERN=''.join(FIVEWEEKPATTERN)
FIVEWEEKPATTERN=FIVEWEEKPATTERN+FOURWEEKPATTERN

#MATCH CURRENT PATTERN WITH PAST PERFORMANCE OF PATTERN

a=0
NOMATCH=0
upHLTWOWK=0
downHLTWOWK=0
TWOWKPATTERNCOUNT=0
while NOMATCH==0:
	if TWOWEEKPATTERN==HIGHLOWWEEK.iloc[a,0]:
         TWOWKPATTERNCOUNT=HIGHLOWWEEK.iloc[a,1]
         upHLTWOWK=HIGHLOWWEEK.iloc[a,2]
         downHLTWOWK=HIGHLOWWEEK.iloc[a,3]
         NOMATCH=1
	else:
		NOMATCH=0
	a+=1

a=0
NOMATCH=0
upHLTREWK=0
downHLTREWK=0
THREEWKPATTERNCOUNT=0
while NOMATCH==0:
	if THREEWEEKPATTERN==HIGHLOWWEEK.iloc[a,0]:
         THREEWKPATTERNCOUNT=HIGHLOWWEEK.iloc[a,1]
         upHLTREWK=HIGHLOWWEEK.iloc[a,2]
         downHLTREWK=HIGHLOWWEEK.iloc[a,3]
         NOMATCH=1
	else:
		NOMATCH=0
	a+=1

a=0
NOMATCH=0
upHLFOURWK=0
downHLFOURWK=0
FOURWKPATTERNCOUNT=0
while NOMATCH==0:
	if FOURWEEKPATTERN==HIGHLOWWEEK.iloc[a,0]:
         FOURWKPATTERNCOUNT=HIGHLOWWEEK.iloc[a,1]
         upHLFOURWK=HIGHLOWWEEK.iloc[a,2]
         downHLFOURWK=HIGHLOWWEEK.iloc[a,3]
         NOMATCH=1
	else:
		NOMATCH=0
	a+=1
a=0
NOMATCH=0
upHLFIVEWK=0
downHLFIVEWK=0
FIVEWKPATTERNCOUNT=0
while NOMATCH==0:
    if FIVEWEEKPATTERN==HIGHLOWWEEK.iloc[a,0]:
        FIVEWKPATTERNCOUNT=HIGHLOWWEEK.iloc[a,1]
        upHLFIVEWK=HIGHLOWWEEK.iloc[a,2]
        downHLFIVEWK=HIGHLOWWEEK.iloc[a,3]
        NOMATCH=1
    elif a==292:
        FIVEPATTERNCOUNT=0
        upHLFIVEWK=0
        downHLFIVEWK=0
        NOMATCH=1
    else:
        NOMATCH=0

    a+=1


HLPATTERNS=DataFrame([TWOWEEKPATTERN,THREEWEEKPATTERN,FOURWEEKPATTERN,FIVEWEEKPATTERN])
HLCOUNT=DataFrame([TWOWKPATTERNCOUNT,THREEWKPATTERNCOUNT,FOURWKPATTERNCOUNT,FIVEWKPATTERNCOUNT])
upHLTWOWK='{0:.0%}'.format(upHLTWOWK)
downHLTWOWK='{0:.0%}'.format(downHLTWOWK)
upHLTREWK='{0:.0%}'.format(upHLTREWK)
downHLTREWK='{0:.0%}'.format(downHLTREWK)
upHLFOURWK='{0:.0%}'.format(upHLFOURWK)
downHLFOURWK='{0:.0%}'.format(downHLFOURWK)
upHLFIVEWK='{0:.0%}'.format(upHLFIVEWK)
downHLFIVEWK='{0:.0%}'.format(downHLFIVEWK)

UPPERF=DataFrame([upHLTWOWK,upHLTREWK,upHLFOURWK,upHLFIVEWK])
DWNPERF=DataFrame([downHLTWOWK,downHLTREWK,downHLFOURWK,downHLFIVEWK])

COLSFINAL=[HLPATTERNS,HLCOUNT,UPPERF,DWNPERF]
FINALDF=pd.concat(COLSFINAL, axis=1)
FINALDF.columns=['PATTERN','OCCURENCES','UP','DOWN']
'''
print ("The last week through the last five weeks have done the following")
print (FINALDF)
'''

conn=sqlite3.connect('WEEKSPATTERN.db')
c= conn.cursor()
c.execute('DROP TABLE IF EXISTS WEEKSPATTERN')
FINALDF.to_sql("WEEKSPATTERN", conn,flavor='sqlite')
FINALDF.to_csv(os.path.expanduser('~/Documents/HTML/WEBWEEKPATTERN.csv'), sep=',')
FIVECHANGES=pd.read_csv(os.path.expanduser("~/Documents/Python/FIVECHANGESWEEK.csv"), sep='\t')
FIVECHANGES=DataFrame(FIVECHANGES)
FIVEPATTERNCHANGE=DataFrame([0]*FIVEWKPATTERNCOUNT)
def fivepatternCHANGE():
    x=0
    y=0
    while x< len(FIVECHANGES):
        if FIVEWEEKPATTERN==FIVECHANGES.iloc[x,1]:
            FIVEPATTERNCHANGE.iloc[y,0]=FIVECHANGES.iloc[x,2]
            y+=1

        x+=1

fivepatternCHANGE()






#year-month-day
SPY=Quandl.get('GOOG/NYSE_SPY',authtoken="vGe9xLEuwzZcGy68aEot")
OPEN=SPY['Open']
HIGH=SPY['High']
LOW=SPY['Low']
CLOSE=SPY['Close']
OPEN=OPEN.iloc[::-1]
HIGH=HIGH.iloc[::-1]
LOW=LOW.iloc[::-1]
CLOSE=CLOSE.iloc[::-1]
OPEN=DataFrame(OPEN.iloc[0:5])
HIGH=DataFrame(HIGH.iloc[0:5])
LOW=DataFrame(LOW.iloc[0:5])
CLOSE=DataFrame(CLOSE.iloc[0:5])
#Create an empty dataframe to fill with last five day pattern
SPYPATTERN=[]*5

def plusminus():
	a=0
	y=0
	for i in range (5):
		if CLOSE.iloc[a,y] > OPEN.iloc[a,y]:
			SPYPATTERN[a:0]='+'
		elif CLOSE.iloc[a,y] < OPEN.iloc[a,y]:
			SPYPATTERN[a:0]='-'
		else:
			SPYPATTERN[a:0]='NEUT'

		a+=1
plusminus()
SPYPATTERN=''.join(SPYPATTERN)
#reverse the string
SPYPATTERN=SPYPATTERN[::-1]
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

TWODAYPATTERN=['0']*2
TWODAYPATTERN=DataFrame(TWODAYPATTERN, columns=['TWODAYPATTERN'])

def TWODAY():
    x=0
    y=1
    if HIGH.iloc[x,0]>HIGH.iloc[y,0]:
        TWODAYPATTERN.iloc[x,0]='HH'
    elif HIGH.iloc[x,0]<HIGH.iloc[y,0]:
        TWODAYPATTERN.iloc[x,0]='LH'
    if LOW.iloc[x,0]<LOW.iloc[y,0]:
        TWODAYPATTERN.iloc[y,0]='LL'
    elif LOW.iloc[x,0]>LOW.iloc[y,0]:
        TWODAYPATTERN.iloc[y,0]='HL'
    if HIGH.iloc[x,0]==HIGH.iloc[y,0]:
        TWODAYPATTERN.iloc[x,0]='00'
    if LOW.iloc[x,0]==LOW.iloc[y,0]:
        TWODAYPATTERN.iloc[y,0]='00'
TWODAY()
TWODAYPATTERN=[TWODAYPATTERN['TWODAYPATTERN'].apply(str)[0],
TWODAYPATTERN['TWODAYPATTERN'].apply(str)[1]]
TWODAYPATTERN=''.join(TWODAYPATTERN)


THREEDAYPATTERN=['0']*2
THREEDAYPATTERN=DataFrame(THREEDAYPATTERN, columns=['THREEDAYPATTERN'])

def THREEDAY():
    z=0
    x=1
    y=2
    if HIGH.iloc[x,0]>HIGH.iloc[y,0]:
        THREEDAYPATTERN.iloc[z,0]='HH'
    elif HIGH.iloc[x,0]<HIGH.iloc[y,0]:
        THREEDAYPATTERN.iloc[z,0]='LH'
    if LOW.iloc[x,0]<LOW.iloc[y,0]:
        THREEDAYPATTERN.iloc[x,0]='LL'
    elif LOW.iloc[x,0]>LOW.iloc[y,0]:
        THREEDAYPATTERN.iloc[x,0]='HL'
    if HIGH.iloc[x,0]==HIGH.iloc[y,0]:
        THREEDAYPATTERN.iloc[z,0]='00'
    if LOW.iloc[x,0]==LOW.iloc[y,0]:
        THREEDAYPATTERN.iloc[x,0]='00'

THREEDAY()
THREEDAYPATTERN=[THREEDAYPATTERN['THREEDAYPATTERN'].apply(str)[0],
THREEDAYPATTERN['THREEDAYPATTERN'].apply(str)[1]]
THREEDAYPATTERN=''.join(THREEDAYPATTERN)
THREEDAYPATTERN=THREEDAYPATTERN+TWODAYPATTERN

FOURDAYPATTERN=['0']*2
FOURDAYPATTERN=DataFrame(FOURDAYPATTERN, columns=['FOURDAYPATTERN'])

def FOURDAY():
    z=0
    a=1
    x=2
    y=3
    if HIGH.iloc[x,0]>HIGH.iloc[y,0]:
        FOURDAYPATTERN.iloc[z,0]='HH'
    elif HIGH.iloc[x,0]<HIGH.iloc[y,0]:
        FOURDAYPATTERN.iloc[z,0]='LH'
    if LOW.iloc[x,0]<LOW.iloc[y,0]:
        FOURDAYPATTERN.iloc[a,0]='LL'
    elif LOW.iloc[x,0]>LOW.iloc[y,0]:
        FOURDAYPATTERN.iloc[a,0]='HL'
    if HIGH.iloc[x,0]==HIGH.iloc[y,0]:
        FOURDAYPATTERN.iloc[z,0]='00'
    if LOW.iloc[x,0]==LOW.iloc[y,0]:
        FOURDAYPATTERN.iloc[a,0]='00'

FOURDAY()
FOURDAYPATTERN=[FOURDAYPATTERN['FOURDAYPATTERN'].apply(str)[0],
FOURDAYPATTERN['FOURDAYPATTERN'].apply(str)[1]]
FOURDAYPATTERN=''.join(FOURDAYPATTERN)
FOURDAYPATTERN=FOURDAYPATTERN+THREEDAYPATTERN

FIVEDAYPATTERN=['0']*2
FIVEDAYPATTERN=DataFrame(FIVEDAYPATTERN, columns=['FIVEDAYPATTERN'])

def FIVEDAY():
    z=0
    a=1
    y=3
    b=4
    if HIGH.iloc[y,0]>HIGH.iloc[b,0]:
        FIVEDAYPATTERN.iloc[z,0]='HH'
    elif HIGH.iloc[y,0]<HIGH.iloc[b,0]:
        FIVEDAYPATTERN.iloc[z,0]='LH'
    if LOW.iloc[y,0]<LOW.iloc[b,0]:
        FIVEDAYPATTERN.iloc[a,0]='LL'
    elif LOW.iloc[y,0]>LOW.iloc[b,0]:
        FIVEDAYPATTERN.iloc[a,0]='HL'
    if HIGH.iloc[y,0]==HIGH.iloc[z,0]:
        FIVEDAYPATTERN.iloc[z,0]='00'
    if LOW.iloc[y,0]==LOW.iloc[b,0]:
        FIVEDAYPATTERN.iloc[a,0]='00'

FIVEDAY()
FIVEDAYPATTERN=[FIVEDAYPATTERN['FIVEDAYPATTERN'].apply(str)[0],
FIVEDAYPATTERN['FIVEDAYPATTERN'].apply(str)[1]]
FIVEDAYPATTERN=''.join(FIVEDAYPATTERN)
FIVEDAYPATTERN=FIVEDAYPATTERN+FOURDAYPATTERN

a=0
NOMATCH=0
upHLTWO=0
downHLTWO=0
TWOPATTERNCOUNT=0
while NOMATCH==0:
	if TWODAYPATTERN==HIGHLOWPATTERNSDF.iloc[a,0]:
         TWOPATTERNCOUNT=HIGHLOWPATTERNSDF.iloc[a,1]
         upHLTWO=HIGHLOWPATTERNSDF.iloc[a,2]
         downHLTWO=HIGHLOWPATTERNSDF.iloc[a,3]
         NOMATCH=1
	else:
		NOMATCH=0
	a+=1

a=0
NOMATCH=0
upHLTRE=0
downHLTRE=0
THREEPATTERNCOUNT=0
while NOMATCH==0:
	if THREEDAYPATTERN==HIGHLOWPATTERNSDF.iloc[a,0]:
         THREEPATTERNCOUNT=HIGHLOWPATTERNSDF.iloc[a,1]
         upHLTRE=HIGHLOWPATTERNSDF.iloc[a,2]
         downHLTRE=HIGHLOWPATTERNSDF.iloc[a,3]
         NOMATCH=1
	else:
		NOMATCH=0
	a+=1

a=0
NOMATCH=0
upHLFOUR=0
downHLFOUR=0
FOURPATTERNCOUNT=0
while NOMATCH==0:
	if FOURDAYPATTERN==HIGHLOWPATTERNSDF.iloc[a,0]:
         FOURPATTERNCOUNT=HIGHLOWPATTERNSDF.iloc[a,1]
         upHLFOUR=HIGHLOWPATTERNSDF.iloc[a,2]
         downHLFOUR=HIGHLOWPATTERNSDF.iloc[a,3]
         NOMATCH=1
	else:
		NOMATCH=0
	a+=1
a=0
NOMATCH=0
upHLFIVE=0
downHLFIVE=0
FIVEPATTERNCOUNT=0
while NOMATCH==0:
    if FIVEDAYPATTERN==HIGHLOWPATTERNSDF.iloc[a,0]:
        FIVEPATTERNCOUNT=HIGHLOWPATTERNSDF.iloc[a,1]
        upHLFIVE=HIGHLOWPATTERNSDF.iloc[a,2]
        downHLFIVE=HIGHLOWPATTERNSDF.iloc[a,3]
        NOMATCH=1
    elif a==1249:
        FIVEPATTERNCOUNT=0
        upHLFIVE=0
        downHLFIVE=0
        NOMATCH=1
    else:
        NOMATCH=0

    a+=1


FIVECHANGESDAY=pd.read_csv(os.path.expanduser("~/Documents/Python/FIVECHANGESDAY.csv"), sep='\t')
FIVECHANGESDAY=DataFrame(FIVECHANGESDAY)
FIVEPATTERNCHANGEDAY=DataFrame([0]*FIVEPATTERNCOUNT)
def fivepatternCHANGEDAY():
    x=0
    y=0
    while x< len(FIVECHANGESDAY):
        if FIVEDAYPATTERN==FIVECHANGESDAY.iloc[x,1]:
            FIVEPATTERNCHANGEDAY.iloc[y,0]=FIVECHANGESDAY.iloc[x,2]
            y+=1

        x+=1

fivepatternCHANGEDAY()



CLCHANGE=(CLNOW-CLOSE.iloc[0,0])/CLOSE.iloc[0,0]
HLPATTERNS=DataFrame([TWODAYPATTERN,THREEDAYPATTERN,FOURDAYPATTERN,FIVEDAYPATTERN])
HLCOUNT=DataFrame([TWOPATTERNCOUNT,THREEPATTERNCOUNT,FOURPATTERNCOUNT,FIVEPATTERNCOUNT])
upHLTWO='{0:.0%}'.format(upHLTWO)
downHLTWO='{0:.0%}'.format(downHLTWO)
upHLTRE='{0:.0%}'.format(upHLTRE)
downHLTRE='{0:.0%}'.format(downHLTRE)
upHLFOUR='{0:.0%}'.format(upHLFOUR)
downHLFOUR='{0:.0%}'.format(downHLFOUR)
upHLFIVE='{0:.0%}'.format(upHLFIVE)
downHLFIVE='{0:.0%}'.format(downHLFIVE)

UPPERF=DataFrame([upHLTWO,upHLTRE,upHLFOUR,upHLFIVE])
DWNPERF=DataFrame([downHLTWO,downHLTRE,downHLFOUR,downHLFIVE])

COLSFINAL=[HLPATTERNS,HLCOUNT,UPPERF,DWNPERF]
FINALDF2=pd.concat(COLSFINAL, axis=1)
FINALDF2.columns=['PATTERN','OCCURENCES','UP','DOWN']
'''
print("The last day through the last five days have done the following")
print(FINALDF2)
'''
conn=sqlite3.connect('DAYSPATTERN.db')
c= conn.cursor()
c.execute('DROP TABLE IF EXISTS DAYSPATTERN')
FINALDF2.to_sql("DAYSPATTERN", conn,flavor='sqlite')
FINALDF2.to_csv(os.path.expanduser('~/Documents/HTML/WEBDAYPATTERN.csv'), sep=',')



SPYPATTERNDF=DataFrame([SPYPATTERN])
up='{0:.0%}'.format(up)
dwn='{0:.0%}'.format(dwn)
updf=DataFrame([up])
dwndf=DataFrame([dwn])
SPYCOLS=[SPYPATTERNDF,updf,dwndf]
SPYDF=pd.concat(SPYCOLS, axis=1)
SPYDF.columns=['PLUSMINUSDAY','UP RATE','DOWN RATE']
'''
print (' ')
print (SPYDF)
#SPY data tested from 1/29/1993 to 3/11/2016")
print (" ")
'''

WEEK=[]
CLWKFIVE=CLWEEK.iloc[0:5]
OPWKFIVE=OPWEEK
CLWKFIVE=CLWKFIVE.iloc[::-1]
OPWKFIVE=OPWKFIVE.iloc[::-1]
def plusminus():
	a=0
	y=0
	for i in range (5):
		if CLWKFIVE.iloc[a,y] > OPWKFIVE.iloc[a,y]:
			WEEK[a:0]='+'
		elif CLWKFIVE.iloc[a,y] < OPWKFIVE.iloc[a,y]:
			WEEK[a:0]='-'
		else:
			WEEK[a:0]='0'

		a+=1
plusminus()
WEEK=''.join(WEEK)
WEEKDF=DataFrame([WEEK])
a=0
NOMATCH=0
up=0
dwn=0
while NOMATCH==0:
    if WEEK==ESWEEKLYPATTERNS.iloc[a,0]:
        up=ESWEEKLYPATTERNS.iloc[a,3]
        dwn=ESWEEKLYPATTERNS.iloc[a,4]
        NOMATCH=1
    elif a ==59:
        up=0
        dwn=0
        NOMATCH=1
    else:
        NOMATCH=0
    a+=1

up='{0:.0%}'.format(up)
dwn='{0:.0%}'.format(dwn)
updf=DataFrame([up])
dwndf=DataFrame([dwn])
WEEKCOLS=[WEEKDF,updf,dwndf]
WEEKDF=pd.concat(WEEKCOLS,axis=1)
WEEKDF.columns=['PLUSMINUSWEEK','UP RATE','DOWN RATE']
'''
print(' ')
print (WEEKDF)
'''

#find the current high low of futures


POSITION=DataFrame([0])
VALUE=FIVEPATTERNCHANGE.mean()*CLWEEK.iloc[0,0]+CLWEEK.iloc[0,0]


WEEKSTDUP=float((VALUE*FIVEPATTERNCHANGE.std())+VALUE)
WEEKSTDDOWN=float(VALUE-(VALUE*FIVEPATTERNCHANGE.std()))


print ("The last week through the last five weeks have done the following")
print (FINALDF)
print (' ')
VALUE=FIVEPATTERNCHANGE.mean()*CLWEEK.iloc[0,0]+CLWEEK.iloc[0,0]
VALUE=DataFrame(VALUE)
print (' ')
print ('Value price based on pattern')
print ("%.2f" % VALUE.iloc[0,0])
print (' ')

print ('One Standard Deviation Up')
print ((VALUE*FIVEPATTERNCHANGE.std())+VALUE)
print (' ')
print ('One Standard Deviation Down')
print (VALUE-(VALUE*FIVEPATTERNCHANGE.std()))

print("The last day through the last five days have done the following")
print(FINALDF2)

print (' ')

VALUE=FIVEPATTERNCHANGEDAY.mean()*CLOSE.iloc[0,0]+CLOSE.iloc[0,0]
VALUE=DataFrame(VALUE)
print (' ')
print ('Value price based on pattern')
print ("%.2f" % VALUE.iloc[0,0])
print (' ')

print ('One Standard Deviation Up')
print ((VALUE*FIVEPATTERNCHANGEDAY.std())+VALUE)
print (' ')
print ('One Standard Deviation Down')
print (VALUE-(VALUE*FIVEPATTERNCHANGEDAY.std()))

print (' ')
print (SPYDF)
#SPY data tested from 1/29/1993 to 3/11/2016")
print (" ")

print(' ')
print (WEEKDF)

