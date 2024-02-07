import streamlit as st
import pytz
import datetime as t

import pandas as pd
import numpy as np
import yfinance as yf

st.title("女神股票監控室")
taiwan_tz = pytz.timezone("Asia/Taipei") #時區
st.write(f":green[{t.datetime.now(taiwan_tz)}]")
st.divider()

def calculate(df):
    maxIndex = len(df['Close'])

    df['TR'] = pd.concat([abs(df['High']-df['Low']),abs(df['High']-df['Close'].shift(1)),abs(df['Low']-df['Close'].shift(1))],axis=1).max(axis=1)
    df['+DM_DFF'] = df['High'].diff()
    df['-DM_DFF'] = -df['Low'].diff()
    df['+DM'] = np.where((df['+DM_DFF'] > df['-DM_DFF']) & (df['+DM_DFF'] > 0), df['+DM_DFF'], 0)#PDM
    df['-DM'] = np.where((df['-DM_DFF'] > df['+DM_DFF']) & (df['-DM_DFF'] > 0), df['-DM_DFF'], 0)#NDM    

    df['FTR'] = df['TR'].rolling(window=14).sum()/14
    df['+FDM'] = df['+DM'].rolling(window=14).sum()/14
    df['-FDM'] = df['-DM'].rolling(window=14).sum()/14

    df['ATR'] = df['FTR']
    df['+ADM'] = df['+FDM']
    df['-ADM'] = df['-FDM']

    df['ATR'][14] = df['FTR'][13]*13/14 + df['TR'][14]*1/14
    df['+ADM'][14] = df['+FDM'][13]*13/14 + df['+DM'][14]*1/14
    df['-ADM'][14] = df['-FDM'][13]*13/14 + df['-DM'][14]*1/14    
    
    for i in range(15,maxIndex):
        df['ATR'][i] = df['ATR'][i-1]*13/14+df['TR'][i]*1/14
        df['+ADM'][i] = df['+ADM'][i-1]*13/14+df['+DM'][i]*1/14
        df['-ADM'][i] = df['-ADM'][i-1]*13/14+df['-DM'][i]*1/14

    df['+DI'] = 100 * df['+ADM'] / df['ATR']
    df['-DI'] = 100 * df['-ADM'] / df['ATR']

    df['DX'] = 100 * abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI'])

    df['FDX'] = df['DX'].rolling(window=14).sum()/14
    df['ADX'] = df['FDX']
    df['ADX'][28] = df['FDX'][27]*13/14 + df['DX'][28]*1/14

    for i in range(29,maxIndex):
        df['ADX'][i] = df['ADX'][i-1]*13/14+df['DX'][i]*1/14

    return df

# 輸入股票代號
stock_id = "2313.TW"
end = t.date.today()  # 資料結束時間
start = end - t.timedelta(days=365)  # 資料起始時間
df = yf.download(stock_id, start=start, end=end).reset_index()  # 抓取股價資料
df = calculate(df)
df1 = pd.DataFrame({
  'Date': pd.to_datetime(df['Date']).dt.strftime('%Y/%m/%d'),
  'Open': df['Open'],
  'High': df['High'],
  'Low': df['Low'],
  'Close': df['Close'],
  '成交量': (df['Volume']/1000).round(0),
  '+DI': (df['+DI']).round(2),
  '-DI': (df['-DI']).round(2),
  'ADX': (df['ADX']).round(2)
})
df1=df1.sort_values('Date',ascending=False)
df1.reset_index(drop=True, inplace=True)
df1
df2 = pd.DataFrame({
    'Date': pd.to_datetime(df['Date']).dt.strftime('%Y/%m/%d'),
    '+DI': df['+DI'],
    '-DI': df['-DI'],
    'ADX': df['ADX']
})
df2=df2.iloc[len(df2['Date'])-50:len(df2['Date'])]
st.line_chart(df2,x='Date')
st.balloons()

