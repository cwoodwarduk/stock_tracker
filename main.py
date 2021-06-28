import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt

from pandas_datareader import data as pdr

yf.pdr_override()

stock = input("Enter a stock ticker symbol: ")
print(stock)

startYear = 2020
startMonth = 1
startDay = 1

start = dt.datetime(startYear, startMonth, startDay)

now = dt.datetime.now()

dataframe = pdr.get_data_yahoo(stock, start, now)

# movingAvg = 50
#
# smaString = "Sma_" + str(movingAvg)
#
# dataframe[smaString] = dataframe.iloc[:,4].rolling(window=movingAvg).mean()
#
# dataframe = dataframe.iloc[movingAvg:]
#

emasUsed = [3,5,8,10,12,15,30,35,40,45,50,60]

for x in emasUsed:
    ema = x
    dataframe["Ema_" + str(ema)] = round(dataframe.iloc[:,4].ewm(span=ema, adjust=False).mean(),2)

# print(dataframe.tail())

isPositionEntered = 0
num = 0
percentChange = []

for i in dataframe.index:
    cmin = min(dataframe["Ema_3"][i],dataframe["Ema_5"][i],dataframe["Ema_8"][i],dataframe["Ema_12"][i],dataframe["Ema_15"][i])
    cmax = max(dataframe["Ema_30"][i],dataframe["Ema_35"][i],dataframe["Ema_40"][i],dataframe["Ema_45"][i],dataframe["Ema_50"][i],dataframe["Ema_60"][i])

    close = dataframe["Adj Close"][i]

    if(cmin > cmax):
        print("Red White Blue")
        if(isPositionEntered == 0):
            buyPrice = close
            isPositionEntered = 1
            print("buying now at " + str(buyPrice))
    elif(cmin<cmax):
        print("Blue White Red")
        if (isPositionEntered == 1):
            sellPrice = close
            isPositionEntered = 0
            print("selling now at " + str(sellPrice))
            newPercentChange = (sellPrice/buyPrice-1)*100
            percentChange.append(newPercentChange)

    num += 1

    if(num == dataframe["Adj Close"].count()-1 and isPositionEntered == 1):
        sellPrice = close
        isPositionEntered = 0
        print("selling now at " + str(sellPrice))
        newPercentChange = (sellPrice / buyPrice - 1) * 100
        percentChange.append(newPercentChange)

print(percentChange)

gains = 0
noOfGains = 0
losses = 0
noOfLosses = 0
totalReturn = 1

for i in percentChange:
    if(i > 0):
        gains += i
        noOfGains += 1
    else:
        losses += i
        noOfLosses += 1

    totalReturn = totalReturn * ((i/100) + 1)

totalReturn = round((totalReturn - 1) * 100, 2)

if(noOfGains > 0):
    averageGain = gains/noOfGains
    maxReturn = str(max(percentChange))
else:
    averageGain = 0
    maxR = "undefined"

if (noOfLosses > 0):
    averageLoss = losses / noOfLosses
    maxLoss = str(min(percentChange))
    ratio = str(-averageGain / averageLoss)
else:
    averageLoss = 0
    maxR = "undefined"
    ratio = "infinite"

if(noOfGains > 0 or noOfLosses > 0):
    battingAverage = noOfGains/(noOfGains+noOfLosses)
else:
    battingAverage = 0

print()
print("Results for " + stock + " going back to " + str(dataframe.index[0]) + ", Sample size: " + str(noOfGains + noOfLosses) + " trades")
print("EMAs used: " + str(emasUsed))
print("Batting Avg: " + str(battingAverage))
print("Gain/loss ratio: " + ratio)
print("Average Gain: " + str(averageGain))
print("Average Loss: " + str(averageLoss))
print("Max Return: " + maxReturn)
print("Max Loss: " + maxLoss)
print("Total return over " + str(noOfGains + noOfLosses) + " trades: " + str(totalReturn) + "%" )
#print("Example return Simulating "+str(n)+ " trades: "+ str(nReturn)+"%" )
print()
