import streamlit as st
import pandas as pd
import datetime as t
import pytz


st.title("股市監控室")
st.header("雞舍:red[溫度]和:blue[光線]狀態")
taiwan_tz = pytz.timezone("Asia/Taipei") #時區
st.write(f":green[{t.datetime.now(taiwan_tz)}]")
st.divider()

data = {'股票': ['華通', '台積電', '聯電', '台燿'],'收盤價': [10, 20, 30, 50]}
df = pd.DataFrame(data,index=['🥰','🥰','🥰','🥰'])
df