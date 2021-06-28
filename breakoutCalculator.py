import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr

yf.pdr_override() # <== that's all it takes :-)
start = dt.datetime(1980,12,1)
now = dt.datetime.now()
stock = ""

stock = input("Enter the stock symbol: ")

while stock != "quit":
  dataframe = pdr.get_data_yahoo(stock, start, now)

  dataframe.drop(dataframe[dataframe["Volume"] < 1000].index, inplace=True)

  dataframeMonth = dataframe.groupby(pd.Grouper(freq="M"))["High"].max()

  greenlineDate = 0
  lastGreenLineValue = 0
  currentDate = ""
  currentGreenLineValue = 0

  for index, value in dataframeMonth.items():
      if value > currentGreenLineValue:
          currentGreenLineValue = value
          currentDate = index
          counter = 0

      if value < currentGreenLineValue:
          counter = counter + 1

          if counter == 3 and ((index.month != now.month) or (index.year != now.year)):
              if currentGreenLineValue != lastGreenLineValue:
                print(currentGreenLineValue)
          greenlineDate = currentDate
          lastGreenLineValue = currentGreenLineValue
          counter = 0

  if lastGreenLineValue == 0:
      message = stock + " has not formed a green line yet"
  else:
      message = ("Last green line: " + str(lastGreenLineValue) + " on " + str(greenlineDate))

  print(message)

  stock = input("Enter the stock symbol: ")
