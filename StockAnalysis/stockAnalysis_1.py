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
    Code as is from == = https://www.kaggle.com/kernels/scriptcontent/4287243/download
    # Relative Strength Index
    # Avg(PriceUp)/(Avg(PriceUP)+Avg(PriceDown)*100
    # Where: PriceUp(t)=1*(Price(t)-Price(t-1)){Price(t)- Price(t-1)>0};
    #        PriceDown(t)=-1*(Price(t)-Price(t-1)){Price(t)- Price(t-1)<0};
    """
    print(values)
    up = values[values>0].mean()
    down = -1*values[values<0].mean()
    rsi = 100 * up / (up + down)
    return rsi

### Create DF's
df_aapl = pd.read_csv(csv_aapl, sep=',')
len_df_aapl = len(df_aapl.index)
#print(df_aapl.head(10))
#print("   "*100)

df_ibm = pd.read_csv(csv_ibm, sep=',')
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
# #

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



"""
Code Dump below here --- 
"""

"""
stockAnalysis_1.py:56: FutureWarning: Currently, 'apply' passes the values as ndarrays to the applied function. In the future, this will change to passing it as Series objects. You need to specify 'raw=True' to keep the current behaviour, and you can pass 'raw=False' to silence this warning
  df_aapl['rsi_14days'] = df_aapl['momentum_1day'].rolling(center=False, window=14).apply(rsi).fillna(0)
[ 1.753e+02 -6.000e-02 -3.970e+00 -2.420e+00 -3.910e+00  7.830e+00
 -4.430e+00 -1.860e+00  1.300e+00 -1.100e+00  1.710e+00  3.220e+00
  1.190e+00 -4.420e+00]
[-0.06 -3.97 -2.42 -3.91  7.83 -4.43 -1.86  1.3  -1.1   1.71  3.22  1.19
 -4.42  1.67]
[-3.97 -2.42 -3.91  7.83 -4.43 -1.86  1.3  -1.1   1.71  3.22  1.19 -4.42
  1.67  3.2 ]

"""