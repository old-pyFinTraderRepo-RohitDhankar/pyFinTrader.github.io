### quick cut-n-dry py script - heavily inspired by = https://www.kaggle.com/kernels/scriptcontent/4287243/download
###  data scraped on my own . 

import numpy as np
import pandas as pd
import os
import random
import copy
import matplotlib.pyplot as plt
import pandas

### this below here needs an ARGPARSE 
### Also running this script from the CLI - reads in the CSV's everytime its run .. 
csv_aapl = "/media/dhankar/Dhankar_1/a4_19/TraderBOT/pyFinTrader/pyFinApp_1/NASDAQ_TickerDATA/StockTicker_AAPL_APPLE_INC_2019-08-23_.csv"
csv_ibm = "/media/dhankar/Dhankar_1/a4_19/TraderBOT/pyFinTrader/pyFinApp_1/NASDAQ_TickerDATA/StockTicker_IBM_2019-08-23_.csv"
#

def rsi(values):
    """
    Function Code as is from == = https://www.kaggle.com/kernels/scriptcontent/4287243/download
    # Relative Strength Index
    # Avg(PriceUp)/(Avg(PriceUP)+Avg(PriceDown)*100
    # Where: PriceUp(t)=1*(Price(t)-Price(t-1)){Price(t)- Price(t-1)>0};
    #        PriceDown(t)=-1*(Price(t)-Price(t-1)){Price(t)- Price(t-1)<0};
    """
    up = values[values>0].mean()
    down = -1*values[values<0].mean()
    rsi = 100 * up / (up + down)
    return rsi

### Create DF's
df_aapl = pd.read_csv(csv_aapl, sep=',')
df_aapl.name = "df_of_Apple"
len_df_aapl = len(df_aapl.index)
#print(df_aapl.head(10))
#print("   "*100)

df_ibm = pd.read_csv(csv_ibm, sep=',')
df_ibm.name = "df_of_IBM"
len_df_ibm = len(df_ibm.index)
#print(df_ibm.head(10))
#print("   "*100)
#
for k in range(len_df_aapl):
    df_aapl['momentum_1day'] = df_aapl['close']-df_aapl['close'].shift(1).fillna(0)
print(df_aapl.head(3))
print(df_aapl.tail(3))
print("   "*100)
#
for k in range(len_df_ibm):
    df_ibm['momentum_1day'] = df_ibm['close']-df_ibm['close'].shift(1).fillna(0)
# print(df_ibm.head(3))
# print(df_ibm.tail(3))
# print("   "*100)

#### Below code takes a 14 Days Rolling Window and calculates the == Relative Strength Index 
# This is done by APPLYING the method == rsi , on each value of the DataFrame's series / column = momentum_1day
#
df_aapl['rsi_14days'] = df_aapl['momentum_1day'].rolling(center=False, window=14).apply(rsi).fillna(0)
print(df_aapl.head(3))
print(df_aapl.tail(3))
print("   "*100)
#
df_ibm['rsi_14days'] = df_ibm['momentum_1day'].rolling(center=False, window=14).apply(rsi).fillna(0)
print(df_ibm.head(3))
print(df_ibm.tail(3))
print("   "*100)
#
import matplotlib.pyplot as plt

def percentChange(df):
    """ Percentage Change from Last Day Price , using Forward Fill to fill missing values"""
    #df["pcntChngClose_ffill"] = df["close"].pct_change(fill_method ='ffill')# default = fill_method ='ffill'
    df["pcntChngClose"] = df["close"].pct_change().fillna(0)# .fillna(0) -- better ?? 
    #df["pChngCls_StdDev"] = df["close"].pct_change().fillna(0)
    #df["pChngCls_StdDev"] = df["pChngCls_StdDev"].std()# 
    df["pcntChngClose"] = df["pcntChngClose"].astype(float).map("{:.2%}".format)
    print ("{}, % Change Close and Open Price from Last Day " .format(str(df.name))) 
    print(df.head(15))
    print(df.tail(15))
    print("   "*100)
    return df

df_aapl = percentChange(df_aapl)
df_ibm = percentChange(df_ibm)
#

"""

Bollinger Bands - envelope MAX and MIN of the MOVING AVERAGE 
As you can see below, Bollinger Bands are elegant lines driven by price fluctuations.

    Middle Band Line = N-period simple moving average (SMA)
    Upper Band Line = N-period SMA + (N-period standard deviation of price x 2)
    Lower Band Line= N-period SMA – (N-period standard deviation of price x 2)
    #
    Middle Band = 20 day moving average
    Upper Band = 20 day moving average + (20 Day standard deviation of price x 2) 
    Lower Band = 20 day moving average - (20 Day standard deviation of price x 2)

The standard value for N is 20.
SOURCE == https://www.tradingsetupsreview.com/reading-price-action-bollinger-bands/
"""
def bollingerBands(df):
    df["30Day_Mov.avg"] = df["close"].rolling(window=20).mean()
    df["30Day_Std.Dev"] = df["close"].rolling(window=20).std()

    df["20Day_Mov.avg"] = df["close"].rolling(window=10).mean()
    df["20Day_Std.Dev"] = df["close"].rolling(window=10).std()
    df['UpperBB'] = df['30Day_Mov.avg'] + (df['30Day_Std.Dev'] * 2)
    df['LowerBB'] = df['30Day_Mov.avg'] - (df['30Day_Std.Dev'] * 2)
    print(df.head(15))
    print(df.tail(15))
    print("   "*100)
    return df
#    
df_aapl = bollingerBands(df_aapl)
df_ibm = bollingerBands(df_ibm)
#
#30 and 20 Day Bollinger Bands - need to create MatplotLib Subplots ,d3.js ,  Bokeh and PlotlyJS Plots 

df_aapl[['open','close', '30Day_Mov.avg', 'UpperBB', 'LowerBB']].plot(figsize=(12,6))
plt.title('30 Days Bollinger Bands for AAPL')
plt.ylabel('Price (USD)')
plt.show()
#
df_aapl[['open','close', '20Day_Mov.avg', 'UpperBB', 'LowerBB']].plot(figsize=(12,6))
plt.title('20 Days Bollinger Bands for AAPL')
plt.ylabel('Price (USD)')
plt.show()
#
df_ibm[['open','close', '30Day_Mov.avg', 'UpperBB', 'LowerBB']].plot(figsize=(12,6))
plt.title('30 Days Bollinger Bands for IBM')
plt.ylabel('Price (USD)')
plt.show()
#
df_ibm[['open','close', '20Day_Mov.avg','UpperBB', 'LowerBB']].plot(figsize=(12,6))
plt.title(' 20 Days Bollinger Bands for IBM')
plt.ylabel('Price (USD)')
plt.show()

# Shading the space between BB
plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(111)
# Get index values for the X axis for IBM DataFrame
x_axis = df_ibm.index.get_level_values(0)
# Plot shaded 20 Day Bollinger Band for IBM
ax.fill_between(x_axis, df_ibm['UpperBB'], df_ibm['LowerBB'], color='grey')
# Plot Adjust Closing Price and Moving Averages
ax.plot(x_axis, df_ibm['close'], color='blue', lw=2)
ax.plot(x_axis, df_ibm['30Day_Mov.avg'], color='black', lw=2)
# Set Title & Show the Image
ax.set_title('30 Days Bollinger Bands for IBM ')
ax.set_xlabel('Date (Year/Month)')
ax.set_ylabel('Price(USD)')
ax.legend()
plt.show()
#
# Shading the space between BB
plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(111)
# Get index values for the X axis for IBM DataFrame
x_axis = df_aapl.index.get_level_values(0)
# Plot shaded 20 Day Bollinger Band for IBM
ax.fill_between(x_axis, df_aapl['UpperBB'], df_aapl['LowerBB'], color='pink')
# Plot Adjust Closing Price and Moving Averages
ax.plot(x_axis, df_aapl['close'], color='blue', lw=2)
ax.plot(x_axis, df_aapl['30Day_Mov.avg'], color='black', lw=2)
# Set Title & Show the Image
ax.set_title('30 Days Bollinger Bands for AAPL - APPLE Inc. ')
ax.set_xlabel('Date (Year/Month)')
ax.set_ylabel('Price(USD)')
ax.legend()
plt.show()