import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import openpyxl as xl
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

yf.pdr_override()
start = dt.datetime(2019,12,1)
now = dt.datetime.now()

root = Tk()
ftypes = [".csv"]
ttl = "Title"
dir1 = '/Users/calum/'
filePath = askopenfilename(filetypes=(("CSV Files","*.csv"),), initialdir=dir1, title=ttl)

stocklist = pd.read_csv(filePath)
stocklist = stocklist.head()

exportList = pd.DataFrame(columns=['Stock', 'RS_Rating', '50 Day MA', '150 Day MA', '52 Week Low', '52 Week High'])

for i in stocklist.index:
    stock = str(stocklist["Symbol"][i])
    RSRating = stocklist["RS Rating"][i]

    try:
        dataframe = pdr.get_data_yahoo(stock, start, now)

        smaUsed = [50, 150, 200]

        for x in smaUsed:
            sma = x
            dataframe["SMA_" + str(sma)] = round(dataframe.iloc[:,4].rolling(window=sma).mean(),2)

        currentClose = dataframe["Adj Close"][-1]
        movingAverage50 = dataframe["SMA_50"][-1]
        movingAverage150 = dataframe["SMA_150"][-1]
        movingAverage200 = dataframe["SMA_200"][-1]
        lowOf52Week = min(dataframe["Adj Close"][-260:])
        highOf52Week = max(dataframe["Adj Close"][-260:])

        try:
            TwentyDayPreviousMovingAverage200 = dataframe["SMA_200"][-20]
        except Exception:
            TwentyDayPreviousMovingAverage200 = 0

        print("Checking " + stock + ".....")

        # Condition 1: Current Price > 150 SMA and > 200 SMA
        conditionOne = True if currentClose > movingAverage150 and currentClose > movingAverage200 else False

        # Condition 2: 150 SMA and > 200 SMA
        conditionTwo = True if movingAverage150 > movingAverage200 else False

        # Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months)
        conditionThree = True if movingAverage200 > TwentyDayPreviousMovingAverage200 else False

        # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
        conditionFour = True if movingAverage50 > movingAverage150 and movingAverage50 > movingAverage200 else False

        # Condition 5: Current Price > 50 SMA
        conditionFive = True if currentClose > movingAverage50 else False

        # Condition 6: Current Price is at least 30% above 52 week low (Many of the best are up 100-300% before coming out of consolidation)
        conditionSix = True if currentClose >= (lowOf52Week * 1.3) else False

        # Condition 7: Current Price is within 25% of 52 week high
        conditionSeven = True if currentClose >= (highOf52Week * 0.75) else False

        # Condition 8: IBD RS rating >70 and the higher the better
        conditionEight = True if RSRating > 70 else False

        conditions = [conditionOne, conditionTwo, conditionThree, conditionFour, conditionFive, conditionSix, conditionSeven, conditionEight]

        conditionsMet = False

        for y in conditions:
            conditionsMet = True if y == True else False

        for y in conditions:
            conditionsMet = True if y == True else False

        if conditionsMet == True:
            exportList = exportList.append({
                'Stock': stock,
                "RS_Rating": RSRating,
                "50 Day MA": movingAverage50,
                "150 Day Ma": movingAverage150,
                "200 Day MA": movingAverage200,
                "52 Week Low": lowOf52Week,
                "52 week High": highOf52Week},
                ignore_index=True
            )

    except Exception:
        print(Exception.args)

print(exportList)

exportList.to_csv(r'/Users/calum/Projects/stock_tracker/screenOut.csv')
