import streamlit as st
import pytz
import datetime as t

import pandas as pd
import numpy as np
import yfinance as yf

st.title("女神股市監控室")
taiwan_tz = pytz.timezone("Asia/Taipei") #時區
st.write(f":green[{t.datetime.now(taiwan_tz)}]")
st.divider()

def calculate(df):
    df['TR'] = pd.concat([df['High']-df['Low'],abs(df['High']-df['Close'].shift(1)),abs(df['Low']-df['Close'].shift(1))],axis=1).max(axis=1)
    df['+DM_DFF'] = df['High'].diff()
    df['-DM_DFF'] = df['Low'].diff()
    df['+DM'] = np.where((df['+DM_DFF'] > df['-DM_DFF']) & (df['+DM_DFF'] > 0), df['+DM_DFF'], 0)
    df['-DM'] = np.where((-df['-DM_DFF'] > df['+DM_DFF']) & (-df['-DM_DFF'] > 0), -df['-DM_DFF'], 0)
    df['TR_S'] = df['TR'].rolling(window=14).sum()
    df['+DM_S'] = df['+DM'].rolling(window=14).sum()
    df['-DM_S'] = df['-DM'].rolling(window=14).sum()
    df['+DI'] = 100 * df['+DM_S'] / df['TR_S']
    df['-DI'] = 100 * df['-DM_S'] / df['TR_S']
    df['DX'] = 100 * abs(df['+DI'] - df['-DI']) / abs(df['+DI'] + df['-DI'])
    df['ADX'] = df['DX'].rolling(window=14).mean()
    return df

# 輸入股票代號
stock_id = "2330.TW"
# 抓取半年資料
end = t.date.today()  # 資料結束時間
start = end - t.timedelta(days=500)  # 資料起始時間
df = yf.download(stock_id, start=start, end=end).reset_index()  # 抓取股價資料
df = calculate(df)
df1 = pd.DataFrame({
  '日期': pd.to_datetime(df['Date']).dt.strftime('%Y/%m/%d'),
  '開': df['Open'],
  '高': df['High'],
  '低': df['Low'],
  '收': df['Close'],
  '成交量': (df['Volume']/1000).round(0),
  # '+DM_DFF': df['+DM_DFF'],
  # '-DM_DFF': df['-DM_DFF'],
  # '+DM': df['+DM'],
  # '-DM': df['-DM'],
  # '+DM_S':df['+DM_S'],
  # '-DM_S': df['-DM_S'],
  # 'TR':df['TR'],
  # 'TR_S':df['TR_S'],
  '+DI': (df['+DI']).round(2),
  '-DI': (df['-DI']).round(2),
  'ADX': df['ADX']
})
#df=df.iloc[30:]
df1=df1.sort_values('日期',ascending=False)
df1.reset_index(drop=True, inplace=True)
df1
df2 = pd.DataFrame({
    'Date': pd.to_datetime(df['Date']).dt.strftime('%Y/%m/%d'),
    '+DI': (df['+DI']).round(2),
  '-DI': (df['-DI']).round(2),
  'ADX': df['ADX']
})
st.line_chart(df2,x='Date')
st.balloons()

