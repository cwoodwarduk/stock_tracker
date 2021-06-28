import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import matplotlib.pyplot as plt
import statistics
import numpy as np
import matplotlib.ticker as mticker

yf.pdr_override()
year = 1980
start = dt.datetime(year, 1, 1)
now = dt.datetime.now()

stock = input("Enter the stock symbol: ")

while stock != "quit":
    fig, ax1 = plt.subplots()

    df = pdr.get_data_yahoo(stock, start, now)

    sma = int(input("Enter an sma: "))

    limit = int(input("Enter a warning limit: "))

    df['SMA' + str(sma)] = df.iloc[:, 4].rolling(window=sma).mean()

    df['PC'] = ((df['Adj Close'] / df['SMA' + str(sma)]) -1) * 100

    mean = df['PC'].mean()

    standDev = df['PC'].std()

    currentExt = df['PC'][-1]

    ydayExt = df['PC'][-2]


    print("mean: " + str(mean))
    print("standDev: " + str(standDev))

    bins = np.arange(-100, 100, 1)

    plt.xlim([df['PC'].min() - 5, df['PC'].max() + 5])

    plt.hist(df['PC'], bins=bins, alpha=.5)

    plt.title(stock + "-- % From " + str(sma) + " SMA Histogram Since " + str(year))
    plt.xlabel('Percent from ' + str(sma) + ' SMA (bin size = 1)')
    plt.ylabel('Count')

    plt.axvline(x=mean, ymin=0, ymax=1, color='k', linestyle='--')
    plt.axvline(x=mean + standDev, ymin=0, ymax=1, color='gray', linestyle='--')
    plt.axvline(x=mean + 2 * standDev, ymin=0, ymax=1, color='gray', linestyle='--')
    plt.axvline(x=mean + 3 * standDev, ymin=0, ymax=1, color='gray', linestyle='--')

    plt.axvline(x=mean - standDev, ymin=0, ymax=1, color='gray', linestyle='--')
    plt.axvline(x=mean - 2 * standDev, ymin=0, ymax=1, color='gray', linestyle='--')
    plt.axvline(x=mean - 3 * standDev, ymin=0, ymax=1, color='gray', linestyle='--')

    plt.axvline(x=currentExt - standDev, ymin=0, ymax=1, color='red')
    plt.axvline(x=ydayExt - 2 * standDev, ymin=0, ymax=1, color='blue')

    ax1.xaxis.set_major_locator(mticker.MaxNLocator(14))

    fig2, ax2 = plt.subplots()

    df = df[-150:]

    df['PC'].plot(label='close', color='k')
    plt.title(stock + "-- % From " + str(sma) + " Over Past 150 Days")
    plt.xlabel('Date')
    plt.ylabel('Percent from ' + str(sma))

    ax2.xaxis.set_major_locator(mticker.MaxNLocator(8))


    plt.axhline(y=limit, xmin=0, xmax=1, color='r')

    plt.show()

    stock = input("Enter the stock symbol: ")

