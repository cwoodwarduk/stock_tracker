import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import numpy as np
from mplfinance.original_flavor import candlestick_ohlc

yf.pdr_override()

smasUsed = [10, 30, 40]

start = dt.datetime(2020, 1, 1) - dt.timedelta(days=max(smasUsed))
now = dt.datetime.now()
stock = input("Enter stock symbol: ")

while stock != "quit":

    prices = pdr.get_data_yahoo(stock, start, now)

    fig, ax1 = plt.subplots()

    for x in smasUsed:

        sma = x
        prices['SMA_' + str(sma)] = prices.iloc[:, 4].rolling(window=sma).mean()

        # Calculate Bollinger Bands
        bollingerBandPeriod = 20
        standardDeviations = 2

        # Calculates sma and creates a column
        prices['SMA' + str(bollingerBandPeriod)] = prices.iloc[:, 4].rolling(window=bollingerBandPeriod).mean()

        # Calculates standard deviation and creates a column
        prices['STDEV'] = prices.iloc[:, 4].rolling(window=bollingerBandPeriod).std()

        # Calculates upper Bollinger band
        prices['UpperBand'] = prices['SMA' + str(bollingerBandPeriod)] + (standardDeviations * prices['STDEV'])

        # Calculates lower Bollinger band
        prices['LowerBand'] = prices['SMA' + str(bollingerBandPeriod)] - (standardDeviations * prices['STDEV'])

        # Creates a date column stores in number format (for OHCL bars)
        prices["Date"] = mdates.date2num(prices.index)


        # Calculate a 10.4.4 stochastic
        period = 10
        K = 4
        D = 4

        # Find high of period
        prices['rollingHigh'] = prices['High'].rolling(window=period).max()

        # Find low of period
        prices['rollingLow'] = prices['Low'].rolling(window=period).min()

        # Find 10.1 stochastic
        prices['stochastic'] = ((prices['Adj Close'] - prices['rollingLow']) /
                                (prices['rollingHigh'] - prices['rollingLow'])) * 100

        # Find 10.4 stochastic
        prices['K'] = prices['stochastic'].rolling(window=K).mean()

        # Find 10.4.4 stochastic
        prices['D'] = prices['K'].rolling(window=D).mean()

        # Create GD column to store green dots
        prices['GD'] = prices['High']

        # Creat OHLC array which will store price data for the candlestick chart
        ohlc = []

        # Delete extra dates
        prices = prices.iloc[max(smasUsed):]

        # Stores dates of Green Dots
        greenDotDates = []

        # Stores values of Green Dots
        greenDotValues = []

        # The previous day's fast stochastic
        lastK = 0

        # The previous day's slow stochastic
        lastD = 0

        # The previous day's lowest price
        lastLow = 0

        # The previous day's close
        lastClose = 0

        # The previous day's lower Bollinger band
        lastLowBB = 0

        # Go through price history to create candlesticks and Green Dots + Blue Dots
        for i in prices.index:
            # Append OHLC prices to make a candlestick
            pricesToAppend = prices['Date'][i], prices['Open'][i], prices['High'][i], prices['Low'][i],\
                             prices['Adj Close'][i], prices['Volume'][i]

            ohlc.append(pricesToAppend)

            # Check for Green Dot
            if prices['K'][i] > prices['D'][i] and lastK < lastD and lastK < 60:
                # Plot Green Dot
                plt.plot(prices['Date'][i], prices['High'][i] + 1, marker='o', ms=4, ls="", color='g')

                # Store Green Dot date
                greenDotDates.append(i)

                # Store Green Dot value
                greenDotValues.append(prices['High'][i])

            # Check for lower Bollinger band bounce
            if ((lastLow < lastLowBB) or (prices['Low'][i] < prices['LowerBand'][i])) and (prices['Adj Close'][i] > lastClose and prices['Adj Close'][i] > prices['LowerBand'][i]) and lastK < 60:
                # Plot Blue Dot
                plt.plot(prices['Date'][i], prices['Low'][i] - 1, marker='o', ms=4, ls="", color='b')

            # Store values
            lastK = prices['K'][i]
            lastD = prices['D'][i]
            lastLow = prices['Low'][i]
            lastClose = prices['Adj Close'][i]
            lastLowBB = prices['LowerBand'][i]

        # Calculate the EMAs for the stated periods and append to dataframe
        for x in smasUsed:
            sma = x

            prices['SMA_' + str(sma)].plot(label='close')

        # Plot Bollinger bands
        prices['UpperBand'].plot(label='close', color='lightgray')
        prices['LowerBand'].plot(label='close', color='lightgray')

        # Plot candlesticks
        candlestick_ohlc(ax1, ohlc, width=.5, colorup='k', colordown='r', alpha=0.75)

        # Change x axis back to datestamps
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        # Add more labels to x axis
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(8))

        # Rotate dates for readability
        plt.tick_params(axis='x', rotation=45)

        # Pivot points
        pivots = []
        dates = []
        count = 0
        lastPivot = 0

        # Set up arrays to iterate through stock prices and their respective dates
        stockRange = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        dateRange = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Iterate through price history
        for i in prices.index:
            # Highest value in the stock prices array
            currentMax = max(stockRange, default=0)

            # Gets the high value from the dataframe
            value = round(prices['High'][i], 2)

            # Cuts the stock prices array to the 9 most recent values and adds the new high value
            stockRange = stockRange[1:9]
            stockRange.append(value)

            # Cuts the date range array to the 9 most recent values and adds the date of the new high value
            dateRange = dateRange[1:9]
            dateRange.append(i)

            # If the maximum value has remained the same add 1 to the count
            if currentMax == max(stockRange, default=0):
                count += 1
            else:
                # Otherwise potential pivot point, so reset the counter
                count = 0

            # If we have a pivot point
            if count == 5:
                # Assigns that max value as the new last pivot
                lastPivot = currentMax

                # Finds the index of that pivot point in the stock prices array
                dateLocation = stockRange.index(lastPivot)

                # Gets the date corresponding to that pivot point
                lastDate = dateRange[dateLocation]

                # Adds the new pivot point to the pivots array
                pivots.append(currentMax)

                # Add the new pivot point date to the date array
                dates.append(lastDate)

            print()

            # Set length of dotted line on chart
            timeDelta = dt.timedelta(days=30)

            # Iterates through pivots
            for index in range(len(pivots)):
                # Plots horizontal line at pivot point
                plt.plot_date([dates[index] - (timeDelta * .075), dates[index] + timeDelta],
                              [pivots[index], pivots[index]],
                              linestyle='--', linewidth=1, marker=',')

                plt.annotate(str(pivots[index]), (mdates.date2num(dates[index]), pivots[index]),
                             xytext=(-10, 7), textcoords='offset points', fontsize=7, arrowprops=dict(arrowstyle='-|>'))

            # Set labels for x and y axes
            plt.xlabel('Date')
            plt.ylabel('Price')

            # Set title
            plt.title(stock + " - Daily")

            # Add margins
            plt.ylim(prices['Low'].min(), prices['High'].max() * 1.05)

            plt.show()

            stock = input('Enter the stock symbol: ')


