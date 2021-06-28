import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt

yf.pdr_override()
start = dt.datetime(2020, 1, 1)
now = dt.datetime.now()

stock = input("Enter the stock symbol: ")

while stock != "quit":
    df = pdr.get_data_yahoo(stock, start, now)

    df["High"].plot(Label="High")

    pivots = []
    dates = []
    count = 0
    lastPivot = 0

    valueRange = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dateRange = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in df.index:
        currentMax = max(valueRange, default=0)
        value = round(df["High"][i], 2)

        valueRange = valueRange[1:9]
        valueRange.append(value)

        dateRange = dateRange[1:9]
        dateRange.append(i)

        if currentMax == max(valueRange, default=0):
            count += 1
        else:
            count = 0

        if count == 5:
            lastPivot = currentMax
            dateLocation = valueRange.index(lastPivot)
            lastDate = dateRange[dateLocation]
            pivots.append(lastPivot)
            dates.append(lastDate)

    print()

    timeDelta = dt.timedelta(days=30)

    for index in range(len(pivots)):
        print(str(pivots[index]) + ": " + str(dates[index]))

        plt.plot_date([dates[index], dates[index] + timeDelta],
                      [pivots[index], pivots[index]],
                      linestyle="-", linewidth=2, marker=",")

    plt.show()

    stock = input("Enter the stock symbol: ")
